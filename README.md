# SFI2: Native Machine Learning for Network Slicing Architectures :computer:

Developed by Rodrigo M.  <br>
[![](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=GitHub%20Pages&logoColor=white)](https://romoreira.github.io)


This project brings the concept of ML-Agent to add intrinsic security for network slicing reference architectures. The idea is based on sidecar containers that are instantiated along with the core architecture.


### Installing Ksniff on Kubernetes cluster

0. Install Pcap: `libpcap-dev`
1. Need to install Krew:

```
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
```
> https://osm-download.etsi.org/ftp/osm-10.0-ten/OSM-MR11-hackfest/presentations/OSM-MR%2311%20Hackfest%20OAI%20Onboarding%20Demo%20-%20Team%20Suny%20Poly%20(Part%202).pdf

2. `export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"`
3. Test the installation: `kubectl krew`
4. Install the sniff: `kubectl krew install sniff`
5. `kubectl sniff -n default ubuntu -p -o captura.pcap`


### Building ML Agent Docker Image (DockerHub)

0. `docker login --username=<username>`
1. `docker build -t mlagent:v2 .`
2. `docker tag mlagent:v2 moreirar/mlagent:v2`
3. `docker push moreirar/mlagent:v2`

### Installing Istio

1. `$ curl -L https://istio.io/downloadIstio | sh -`
2. `cd <istio_folder>`
3. `istioctl install --set profile=demo -y`
4. `kubectl label namespace default istio-injection=enabled`

## Clone this repo to the Kubernetes Master Node

1. `git clone https://github.com/romoreira/SFI2-Cassandra.git`
2. `cd SFI2-Cassandra`

### Deploying Cassandra on Kubernetes

1. `kubectl apply -f pvc-cassandra.yaml`
2. `kubectl apply -f svc-cassandra.yaml`
3. `kubectl apply -f sts-cassandra.yaml`

### Deploying MLAgent on Kubernetes

1. `kubectl apply -f dep-mlagent.yaml`
2. `kubectl apply -f mlagent-svc.yaml`

### Mirroring Traffic of Cassandra to MLAgent through Istio

1. `kubectl apply -f virtual-service.yaml`


## Financial Support :moneybag:

* [FAPESP](https://fapesp.br/)


### How to cite this work? :newspaper:

```bibtex
@inproceedings{moreira2023,
author = {Rodrigo Moreira and Tereza Carvalho and Flávio Silva},
title = {Designing and Evaluating a high-reliable and security-aware Identity and Access Management for Slicing Architectures},
booktitle = {Anais do XIV Workshop de Pesquisa Experimental da Internet do Futuro},
location = {Brasília/DF},
year = {2023},
issn = {2595-2692},
pages = {1--6},
publisher = {SBC},
address = {Porto Alegre, RS, Brasil},
doi = {10.5753/wpeif.2023.722},
url = {https://sol.sbc.org.br/index.php/wpeif/article/view/24653}
}
```
