# congenial-ipv6-machine
benchmarking inter-az dto with http

We simulated inter-AZ data transfer by performing HTTP GET requests against a cluster of Apache HTTP servers through an internal K8s service load balancer.

### deploy two clusters with single managed node group each configured with 100 m5.4xl; one with ipv4 and the other with ipv6
- addons: kube-proxy (v1.29.0-eksbuild.1) , CoreDNS (v1.11.1-eksbuild.4), Amazon EKS Pod Identity Agent (v1.3.2-eksbuild.2), Amazon CloudWatch Observability (v2.1.3-eksbuild.1)
### deploy apache server with k8s internal service
ipv4 - `kubectl apply -f apache-deploy-ipv4.yaml`
ipv6 - `kubectl apply -f apache-deploy-ipv6.yaml`
### deploy curl clients 
ipv4 - `kubectl apply -f curl-deploy-ipv4.yaml`
ipv6 - `kubectl apply -f curl-deploy-ipv6.yaml`
### set the managed node groups size on both clusters to 110; run on both clusters
```
kubectl get no -L beta.kubernetes.io/instance-type| awk '{print $NF}'| sort | uniq -c
   1 INSTANCE-TYPE
 108 m5.4xlarge
   2 m5.xlarge
```
### let the baseline load shapes run for at least 30 minutes to allow enough data

```
congenial-ipv6-machine]$kubectl config use-context yahavb@ipv6-usw2.us-west-2.eksctl.io 
Switched to context "yahavb@ipv6-usw2.us-west-2.eksctl.io".
[congenial-ipv6-machine]$kubectl get deploy
NAME                READY       UP-TO-DATE   AVAILABLE   AGE
apache-deployment   500/500     500          500         20h
curl-deployment     5000/5000   5000         5000        20h
[congenial-ipv6-machine]$kubectl get po | awk '{print $3}'| sort | uniq -c
5500 Running
   1 STATUS
kubectl get no -L beta.kubernetes.io/instance-type| awk '{print $NF}'| sort | uniq -c
   1 INSTANCE-TYPE
 108 m5.4xlarge
   2 m5.xlarge
[congenial-ipv6-machine]$kubectl config use-context yahavb@pv4-usw2.us-west-2.eksctl.io 
Switched to context "yahavb@ipv4-usw2.us-west-2.eksctl.io".
[congenial-ipv6-machine]$kubectl get deploy
NAME                READY       UP-TO-DATE   AVAILABLE   AGE
apache-deployment   500/500     500          500         24h
curl-deployment     5000/5000   5000         5000        24h
[congenial-ipv6-machine]$kubectl get po | awk '{print $3}'| sort | uniq -c
5500 Running
   1 STATUS
kubectl get no -L beta.kubernetes.io/instance-type| awk '{print $NF}'| sort | uniq -c
   1 INSTANCE-TYPE
 108 m5.4xlarge
   2 m5.xlarge
```

### use you favorite observability tool, Amazon CloudWatch Observability, in our case to discover the `pod_network_tx_bytes` and `pod_network_rx_bytes` per cluster deployment, ipv4 and ipv6.
ensure that `tx` and `rx` rates on both server and client for ipv4 and ipv6 are comparable before analyzing data transfer cost.

### enable two flow logs to two clusters vpcs to cloudwatch logs so we can run LogInisghts stats for top network producers and consumers.


