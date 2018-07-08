# Kubernetes deploy for Prometheus and Grafana

This would create separate namespace `monitoring` and setup such components to it:
- Prometheus
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- Grafana

And configure them to work together.  
One line installation is:
```
kubectl apply -f https://raw.githubusercontent.com/sepich/kubernetes-prometheus/master/monitoring-compiled.yml
```
To cleanup everything, just drop `monitoring` namespace:
```
kubectl delete namespace monitoring
```

## Development
Grafana access is anonymous with admin permissions (reverse-proxy configuration). Tune your desired way to access it in `/grafana/deployment.yml`

Add dashboards to `/grafana/dashboards/` folder.

When ready - compile and deploy:
```
./build.sh
kubectl apply -f monitoring-compiled.yml
```