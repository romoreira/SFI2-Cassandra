# SFI2 Cassandra

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
