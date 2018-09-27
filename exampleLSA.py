from brightway2 import *
import zipfile, os
from bw2data.utils import download_file

def initProject(projectname):
    # Init project and DB
    projects.set_current(projectname)
    bw2setup()
    filepath = download_file("forwast.bw2package.zip", url="http://lca-net.com/wp-content/uploads/")
    dirpath = os.path.dirname(filepath)
    zipfile.ZipFile(filepath).extractall(dirpath)
    BW2Package.import_file(os.path.join(dirpath, "forwast.bw2package"))

def initLCA(method_key, activity_key):
    # Defining the system
    return LCA({activity_key: 1}, method_key)


from lsa import lsa
if __name__ == "__main__":
    initProject("Local Sensitivity Analysis demo")
    lca = initLCA(
        ('ReCiPe Endpoint (I,A)', 'ecosystem quality', 'total'),
        Database("forwast").search('Wood products EU27')[0]
        )
    rsca_summary, rscb_summary = lsa(lca)
