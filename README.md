# SFI2 Cassandra

### Building ML Agent Docker Image (DockerHub)

0. `docker login --username=<username>`
1. `docker build -t mlagent:v2 .`
2. `docker tag mlagent:v2 moreirar/mlagent:v2`
3. `docker push moreirar/mlagent:v2`

### Deploying MLAgent on Kubernetes

1. `kubectl apply -f dep-mlagent.yaml`
2. `kubectl apply -f mlagent-svc.yaml`

### Deploying Cassandra on Kubernetes

1. `kubectl apply -f pvc-cassandra.yaml`
2. `kubectl apply -f svc-cassandra.yaml`
3. `kubectl apply -f sts-cassandra.yaml`

### Installing Istio

1. `$ curl -L https://istio.io/downloadIstio | sh -`
2. `cd istio-1.17.3`
3. `istioctl install --set profile=demo -y`
4. `kubectl label namespace default istio-injection=enabled`

### Mirroring Traffic of Cassandra to MLAgent through Istio

1. `kubectl apply -f virtual-service.yaml`