# SFI2 Cassandra

Installing Istio

1. `$ curl -L https://istio.io/downloadIstio | sh -`
2. `cd istio-1.17.3`
3. `istioctl install --set profile=demo -y`
4. `kubectl label namespace default istio-injection=enabled`
