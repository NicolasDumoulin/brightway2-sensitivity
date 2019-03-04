from brightway2 import Database, LCA
import numpy as np
from pandas import DataFrame
from SALib.sample import morris as ms
from SALib.analyze import morris as ma
import multiprocessing
import pyprind
import math

class ParallelGSALCA:
    '''
    This class will generate the Morris sample and perform lcia computations using multiprocessing feature.
    '''
    def __init__(self, demand, method, morris_problem):
        self.demand = demand
        self.method = method
        # TODO generate morris_problem instead of parameter
        self.morris_problem = morris_problem
    def single_worker(self, sample):
        '''
        Computes the lcia impacts for the given data sampling corresponding to the initial morris problem.
        Returns an array containing the aggregated score and then the impacts for each category.
        '''
        lca = LCA(self.demand, self.method)
        lca.load_lci_data()
        if lca.lcia:
            lca.load_lcia_data()
        if lca.weighting:
            lca.load_weighting_data
        for a_ij, value in zip(self.A_indices, sample[:len(self.A_indices)]):
            #print('aij',tuple(a_ij),value, lca.technosphere_matrix[tuple(a_ij)])
            lca.technosphere_matrix[tuple(a_ij)] = value
            #print(lca.technosphere_matrix[tuple(a_ij)])
        for b_ij, value in zip(self.B_indices, sample[len(self.A_indices):]):
            #print('bij',tuple(b_ij),value)
            lca.biosphere_matrix[tuple(b_ij)] = value
        if not hasattr(lca, "demand_array"):
            lca.build_demand_array()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lca.lci_calculation()
        if lca.lcia:
            lca.lcia_calculation()
        return np.concatenate(([lca.score], np.array(lca.characterized_inventory.sum(axis=1).ravel())[0]))
    def gsa(self, nb_impacts, A_indices, B_indices, number_of_trajectories, progressBar=True, cpus=None, chunk_size=None):
        '''
        Samples the A and B element using Morris method and return the computed impact
        for the aggregated score and then for each category of impact.
        '''
        self.A_indices = A_indices
        self.B_indices = B_indices
        cpus = cpus or multiprocessing.cpu_count()
        # TODO propose an automatic number_of_trajectories
        self.samples = ms.sample(self.morris_problem, number_of_trajectories, num_levels=4)
        if chunk_size:
            self.chunk_size = chunk_size
        else:
            self.chunk_size = max(cpus, number_of_trajectories // 100)
        pool = multiprocessing.Pool(processes=cpus)
        if progressBar:
            bar = pyprind.ProgBar(max(1,math.ceil(len(self.samples)/self.chunk_size)))
        chunks = []
        scores = [[] for i in range(1 + nb_impacts)]
        # store in 'stores' all the mid-point impact
        for sample in self.samples:
            chunks.append(sample)
            if len(chunks) == self.chunk_size:
                for i,result_by_impact in enumerate(map(list,zip(*pool.map(self.single_worker, chunks)))):
                    scores[i] += result_by_impact
                if progressBar:
                    bar.update()
                chunks=[]
        if len(chunks):
            for i,result_by_impact in enumerate(map(list,zip(*pool.map(self.single_worker, chunks)))):
                scores[i] += result_by_impact
            if progressBar:
                bar.update()
            chunks=[]
        self.scores = scores
        return scores
    def gsa_analyse(self):
        return [ma.analyze(self.morris_problem, self.samples, np.array(score), num_levels=4) for score in self.scores]

def gsa(lca, rsca_summary, rscb_summary, number_of_trajectories = 100, progressBar=False):
    # Binding RSC results and uncertainties
    A_indices = np.array(np.array(rsca_summary)[:,1:3],int).tolist()
    B_indices = np.array(np.array(rscb_summary)[:,1:3],int).tolist()
    tech_df = DataFrame.from_records(lca.tech_params)
    bio_df = DataFrame.from_records(lca.bio_params)
    # Dirty patch for elements without min and max values FIXME
    A_indices = [a for a in A_indices if len(tech_df[(tech_df.type==1) & (tech_df.row==a[0]) & (tech_df.col==a[1])])>0]
    B_indices = [b for b in B_indices if len(bio_df[(bio_df.type==2) & (bio_df.row==b[0]) & (bio_df.col==b[1])])>0]
    rev_activity, rev_product, rev_bio = lca.reverse_dict()
    morris_problem = {
        'num_vars':len(A_indices)+len(B_indices),
        'names':[],
        'bounds':[],
        'groups':None
    }
    morris_problem['names'] += [
        'Technosphere '+ str(Database(rev_activity[x[0]][0]).get(rev_activity[x[0]][1])) + ' x ' + str(Database(rev_product[x[1]][0]).get(rev_product[x[1]][1]))
        for x in A_indices
        ]
    morris_problem['names'] += [
        'Biosphere '+str(Database(rev_bio[x[0]][0]).get(rev_bio[x[0]][1])) + ' x ' + str(Database(rev_activity[x[1]][0]).get(rev_activity[x[1]][1]))
        for x in B_indices
        ]
    # retrieve min and max values for populating morris_problem['bounds']
    tech_df = DataFrame.from_records(lca.tech_params)
    bio_df = DataFrame.from_records(lca.bio_params)
    morris_problem['bounds'] = [
            tech_df[(tech_df.type==1) & (tech_df.row==a_ij[0]) & (tech_df.col==a_ij[1])][['minimum','maximum']].values[0]
            for a_ij in A_indices
        ] + [
            bio_df[(bio_df.type==2) & (bio_df.row==b_ij[0]) & (bio_df.col==b_ij[1])][['minimum','maximum']].values[0]
            for b_ij in B_indices
        ]
    gsalca = ParallelGSALCA(lca.demand, lca.method, morris_problem)
    gsalca.gsa(lca.characterization_matrix.shape[0], A_indices, B_indices, number_of_trajectories = 100, progressBar=progressBar)
    return gsalca.gsa_analyse()
