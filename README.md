# k8s monitoring

This would create separate namespace `monitoring` and setup such components to it:
- Prometheus
- Prometheus node-exporter
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- Grafana (`dev0` only)
- Thanos-sidecar 
- git-sync (would live-update Prometheus Alerting rules on new commits to this repo)

And configure them to work together.  
One line installation is:
```
./run deploy [kubeconfig]
```
To cleanup everything, just drop `monitoring` namespace:
```bash
kubectl delete namespace monitoring
# or
./run clean [kubeconfig]
```

## Development
Configure pre-commit githook to test prometheus rules:
```
./run githook
```
This should be done once only.  
You can run tests manually:
```
./run test
```
Alerts convention:  
 - Alerts group name should be equal to filename, one group per file
 - Label `severity` should exist and be: [informational, warning, minor, major, critical]
 - `for` should be set for at least a minute
 - Avoid `annotations.value` if possible, better use `{{printf "%.2f" $value}}` in `annotations.description`
 - Duplicate alerts should have different severities (which will inhibit)
 - Alerta deduplicates on `Env-Resource-Event`, which is `environment-instance-alertname` in prometheus. If it is undesirable - set `labels.instance` to some uniq label, or list all items in `annotations.description` as:
```  
  expr: avg without(instance)(up{job="node"}) < 0.5
  annotations:
    description: >
      Down instances: {{ range query "up{job=\"node\"} == 0" }}
        {{ .Labels.instance }}
      {{ end }}”
```