import rpy2.robjects as robjects
from source import sampling as spl
from source import CauAcc as acc
import sys

robjects.r('''
dag2pag_p <- function(g,L=c()){
  ## create the graph
  # set.seed(78)

  ## compute the true covariance matrix of g
  cov.mat <- trueCov(g)
  ## transform covariance matrix into a correlation matrix
  true.corr <- cov2cor(cov.mat)

  ## Find PAG
  ## as dependence "oracle", we use the true correlation matrix in
  ## gaussCItest() with a large "virtual sample size" and a large alpha:
  system.time(
    true.pag <- dag2pag(suffStat = list(C = true.corr, n = 10^9),
                        indepTest = gaussCItest,
                        graph=g, L=L, alpha = 0.9999) )
  return(true.pag)
}
''')

# R package names
packnames = ('ggplot2', 'hexbin', 'pcalg')

# import rpy2's package module
import rpy2.robjects.packages as rpackages

if all(rpackages.isinstalled(x) for x in packnames):
    have_tutorial_packages = True
else:
    have_tutorial_packages = False

if not have_tutorial_packages:
    # import R's utility package
    utils = rpackages.importr('utils')
    # select a mirror for R packages
    utils.chooseCRANmirror(ind=1)  # select the first mirror in the list
if not have_tutorial_packages:
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
    # file
    packnames_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
    if len(packnames_to_install) > 0:
        utils.install_packages(StrVector(packnames_to_install))


def main():
    dag_GT = acc.load_graph_true_graph()
    r_f = robjects.r['dag2pag_p']
    res = r_f(dag_GT)
    print(res)

if __name__ == '__main__':
    main()




