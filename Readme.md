# BrightWay2 sensitivity

This project aims to propose a module for brightway2 that implements methods of sensitivity analysis proposed in [the article of (Wei et al., 2015)](http://pubs.acs.org/doi/abs/10.1021/es502128k).

## Using BrightWay2 with docker

A docker image [is available](https://github.com/cmutel/bw2-docker) and allow to easily run a notebook with BrightWay2. See the [documentation of the jupyter docker image](https://github.com/jupyter/docker-stacks/tree/master/minimal-notebook) for launching options.

```
docker pull cmutel/brightway2
docker run -it --rm -p 8888:8888 --volume=$(pwd):/home/jovyan/notebooks cmutel/brightway2
```
