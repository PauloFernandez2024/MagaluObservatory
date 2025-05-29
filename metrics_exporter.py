from prometheus_client import Gauge, CollectorRegistry, push_to_gateway

registry = CollectorRegistry()
health_metric = Gauge("network_device_health", "Health status of network device", ["device", "window", "metric", "category", "status"], registry=registry)

def export_health(device, window, metric, status, category):
    health_metric.labels(device=device, window=window, metric=metric, category=category, status=status).set(1)
    push_to_gateway("http://localhost:9091", job="network_health", registry=registry)
