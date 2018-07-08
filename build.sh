#!/bin/bash
res='monitoring-compiled.yml'
echo -n "Generating $res..."

echo '' > "$res"
for f in `find . -mindepth 2 -maxdepth 2 -type f -name '*.yml' | sort -t/ -k3`; do
    echo "---" >> "$res"
    cat "$f" >> "$res"
done

echo "---" >> "$res"
kubectl -n monitoring create configmap prometheus-config --from-file=prometheus/etc/prometheus.yml -o yaml --dry-run >> "$res"

echo "---" >> "$res"
kubectl -n monitoring create configmap grafana-dashboards --from-file=grafana/dashboards -o yaml --dry-run >> "$res"

echo "done"