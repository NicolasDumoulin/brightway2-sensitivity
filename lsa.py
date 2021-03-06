# -*- coding: utf-8

from brightway2 import Database
import numpy as np
try:
    from pypardiso import factorized, spsolve
except ImportError:
    from scipy.sparse.linalg import factorized, spsolve
from scipy.sparse import csr_matrix


def lsa(lca, threshold=0.1):
    '''
    Computes relative sensitivity coefficients (RSC) according to (Heijungs and Kleijn, 2001) and (Sakai and Yokoyama, 2002), used in (Wei et al., 2015) for performing a local sensitivity analysis.
    Returns an array of two datasets of RSC, respectively for the technosphere and the biosphere matrices, where each record contains:
     - impact indix
     - row index in the matrix
     - column index in the matrix
     - value of RSC
     - label of the row (respectively activity and biosphere)
     - label of the column (respectively product and activity)

    Only RSC above the given threshold will be keeped.

    References:
     Heijungs, R.; Kleijn, R. Numerical approaches towards life cycle interpretation five examples. Int. J. Life Cycle Assess. 2001, 6, 141−148.
     Sakai, S.; Yokoyama, K. Formulation of sensitivity analysis in life
cycle assessment using a perturbation method. Clean Technol. Environ.
Policy 2002, 4, 72−78
     W. Wei, P. Larrey Lassalle, T. Faure, N. Dumoulin, P. Roux, J.D. Mathias. How to conduct a proper sensitivity analysis in life cycle assessment: Taking into account correlations within LCI data and interactions within the LCA calculation model Environmental Science & Technology 49 (1), 2015 http://pubs.acs.org/doi/abs/10.1021/es502128k
    '''
    lca.lci()
    lca.lcia()
    m_a = lca.technosphere_matrix
    m_b = lca.biosphere_matrix
    m_q = lca.characterization_matrix
    h = lca.characterized_inventory.sum(axis=1)
    s = lca.supply_array
    m_lambda = spsolve(m_a.transpose(),m_b.transpose()).transpose()
    m_ql = m_q.dot(m_lambda)
    rev_activity, rev_product, rev_bio = lca.reverse_dict()
    m_as = m_a.multiply(s)
    rsca = [-m_as.multiply(1/hk).multiply(m_ql[k,:]).tocsr() for k,hk in enumerate(h)]
    rscb = [m_b.multiply(1/hk).multiply(m_q[k,:].T).multiply(s).tocsr() for k,hk in enumerate(h)]
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
