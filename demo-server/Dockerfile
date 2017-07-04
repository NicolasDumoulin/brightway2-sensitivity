FROM cmutel/brightway2

MAINTAINER Nicolas Dumoulin <nicolas.dumoulin@irstea.fr>

USER root

RUN pip install --upgrade pip

USER $NB_USER

# Jupyter nice extensions
# RUN pip install jupyter_contrib_nbextensions
# RUN jupyter contrib nbextension install --user
# RUN jupyter nbextensions_configurator enable --user
#
# # sensitivity analysis module
# RUN pip install SALib
#
# # fiability module
# RUN conda install -y -c conda-forge openturns
#
# # Plotting features for jupyter (interactive in the web browser)
# RUN conda install -y -c conda-forge bqplot
# RUN pip install plotly mpld3

RUN mkdir $HOME/sensitivity

# Set the password of the notebook
RUN echo >> $HOME/.jupyter/jupyter_notebook_config.py
RUN echo 'c.NotebookApp.password =u"sha1:d8475d11920b:a1476c34fa69eca2e097f5d9649fb7c9d75d319c"' >> $HOME/.jupyter/jupyter_notebook_config.py

#RUN echo 'c.NotebookApp.base_url = "/bw2/"' >> $HOME/.jupyter/jupyter_notebook_config.py
RUN echo 'c.NotebookApp.allow_origin = "*"' >> $HOME/.jupyter/jupyter_notebook_config.py
RUN echo 'c.Application.log_level = "DEBUG"' >> $HOME/.jupyter/jupyter_notebook_config.py

# Add our python modules in python path
RUN mkdir -p $HOME/.ipython/profile_default/startup
COPY sensitivity-import.py $HOME/.ipython/profile_default/startup/
