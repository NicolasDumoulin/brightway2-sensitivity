from brightway2 import Database
import numpy as np
try:
    from pypardiso import factorized, spsolve
except ImportError:
    from scipy.sparse.linalg import factorized, spsolve
from scipy.sparse import csr_matrix


def lsa(lca, threshold=0.1):
    lca.lci()
    lca.lcia()
    m_a = lca.technosphere_matrix
    m_b = lca.biosphere_matrix
    m_q = lca.characterization_matrix
    h = lca.characterized_inventory.sum(axis=1)
    s = lca.supply_array
    m_lambda = spsolve(m_a.transpose(),m_b.transpose()).transpose()
    m_ql = np.dot(m_q, m_lambda)
    rev_activity, rev_product, rev_bio = lca.reverse_dict()
    rsca = [-csr_matrix(s).multiply(m_ql[k,:].transpose().multiply(m_a)).multiply(1/hk) for k,hk in enumerate(h)]
    rscb = [m_q[k,:].transpose().multiply(m_b).multiply(csr_matrix(s)).multiply(1/hk) for k,hk in enumerate(h)]
    rsca_filtered = [[k, x[0],x[1],rscak[x[0],x[1]]] for k,rscak in enumerate(rsca) for x in np.array(rscak.nonzero()).T  if abs(rscak[x[0],x[1]])>threshold]
    rsca_sorted = sorted(rsca_filtered, key=lambda x:abs(x[3]), reverse=True)
    rsca_summary = [x+[
        str(Database(rev_activity[x[1]][0]).get(rev_activity[x[1]][1])),
        str(Database(rev_product[x[2]][0]).get(rev_product[x[2]][1]))] for x in rsca_sorted]
    rscb_filtered = [[k, x[0],x[1],rscbk[x[0],x[1]]] for k,rscbk in enumerate(rscb) for x in np.array(rscbk.nonzero()).T  if abs(rscbk[x[0],x[1]])>threshold]
    rscb_sorted = sorted(rscb_filtered, key=lambda x:abs(x[3]), reverse=True)
    rscb_summary = [x+[
            str(Database(rev_bio[x[1]][0]).get(rev_bio[x[1]][1])),
            str(Database(rev_activity[x[2]][0]).get(rev_activity[x[2]][1]))] for x in rscb_sorted]
    return [rsca_summary, rscb_summary]