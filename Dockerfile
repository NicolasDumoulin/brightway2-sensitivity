FROM cmutel/brightway2

MAINTAINER Nicolas Dumoulin <nicolas.dumoulin@irstea.fr>

USER $NB_USER

RUN pip install --upgrade pip

# Jupyter nice extensions
RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user

# dependencies (including sensitivity analysis module)
ADD pip-requires.txt /home/jovyan/pip-requires.txt
RUN pip install -r /home/jovyan/pip-requires.txt

# fiability module
RUN conda install -y -c conda-forge openturns

# Plotting features for jupyter (interactive in the web browser)
RUN conda install -y -c conda-forge bqplot
RUN pip install plotly mpld3
