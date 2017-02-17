FROM cmutel/brightway2

MAINTAINER Nicolas Dumoulin <nicolas.dumoulin@irstea.fr>

USER $NB_USER

RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user
