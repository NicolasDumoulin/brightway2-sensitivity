# BrightWay2 sensitivity

This project aims to propose a module for brightway2 that implements methods of sensitivity analysis proposed in [the article of (Wei et al., 2015)](http://pubs.acs.org/doi/abs/10.1021/es502128k).

## Python module

We provide a python module ```lsa.py``` for achieving a local sensitivity analysis.

## Working with virtualenv

```
virtualenv env
source env/bin/activate
pip install -r pip-requires.txt
```

You should then be able to run LSA example:
```
python exampleLSA.py
```
It should write two output files that gives the relative sensitivity coefficients (RSC): exampleLSA_rsca.csv and exampleLSA_rscb.csv

## Using BrightWay2 with docker

A docker image [is available](https://github.com/cmutel/bw2-docker) and allow to easily run a notebook with BrightWay2. See the [documentation of the jupyter docker image](https://github.com/jupyter/docker-stacks/tree/master/minimal-notebook) for launching options.

```
docker pull cmutel/brightway2
docker run -it --rm -p 8888:8888 --volume=$(pwd):/home/jovyan/notebooks cmutel/brightway2
```

You can also use the enhanced version that I propose, that add the [Jupyter notebook extensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions) with a lot of features for the notebook. For that:
```
docker build -t bw2 .
docker run -it --rm -p 8888:8888 --volume=$(pwd):/home/jovyan/notebooks bw2
```

## TODO
- Deploy a test instance for easy demonstration and contact Philippe, Pyrenne and Éléonore on 2/06
  - example with sample data
  - guide for describing a model in brightway2
- Is the factor's selection pertinent after the LSA (threshold=0.1)?
  - maybe fix instead a fixed number of factor (for example 50 or 100)
- Some missing uncertainties in section 1.5 (fixme). To see with Chris Mutel
- Which is the best GSA indicator among mu and mu_star? Are the errors relevant on the charts?
  - test with higher number of simulations
- Produce a python module as lsa.py with an easy access to GSA
- Produce a procedure for installation on windows
- import EcoInvent data
