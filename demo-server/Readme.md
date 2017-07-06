### Usage

To use our module with this demo server, you need to import it:
```
import lsa, gsa
```

If the module has been updated, you can either reload the python kernel from your notebook, or add
this script to be aware of any module update:
```
%load_ext autoreload
%autoreload 2
```

### Installation notes

  * On `cfp6078`, create a user, and add it to the group `docker`
```
sudo adduser --disabled-password bw2
sudo usermod -G docker bw2
```
  * Add authorized SSH keys in `~bw2/.ssh/authorized_keysauthorized_keys`.
  * Deploy the parent directory (`brightway2-sensitivity` root of the git project including python modules) from your computer to `cfp6078`
```
rsync -Cauvb ../ bw2@cfp6078:brightway2-sensitivity/
```
  * Generate a password and put it in the Dockerfile
```
python -c 'from IPython.lib import passwd; print(passwd("secret"))'
```
  * From the directory `demo-server` on the server `cfp6078`, build the docker image
```
docker build -t bw2-uncertainty-demo .
```
  * Create a network for isolate the docker container from the network
```
docker network create -o com.docker.network.bridge.enable_icc=false -o com.docker.network.bridge.enable_ip_masquerade=false isolated
```
  * Run the container
```
docker run -it -d -p 8888:8888 --network=isolated --volume=/home/bw2/brightway2-sensitivity/demo-server/notebooks:/home/jovyan/notebooks --volume=/home/bw2/brightway2-sensitivity:/home/jovyan/sensitivity bw2-uncertainty-demo
```
