from prometheus_client import Gauge, CollectorRegistry, push_to_gateway

def get_health_gauges(extra_labels):
    base_labels = ["device", "window", "metric", "category", "job", "status"]
    all_labels = base_labels + extra_labels
    registry = CollectorRegistry()

    return {
        "status": Gauge("device_health_status", "Health status of monitored device", all_labels, registry=registry),
        "mean": Gauge("device_health_value_mean", "Mean value of computed health metric", all_labels[:-1], registry=registry),
        "max": Gauge("device_health_value_max", "Max value of computed health metric", all_labels[:-1], registry=registry),
        "min": Gauge("device_health_value_min", "Min value of computed health metric", all_labels[:-1], registry=registry),
        "std": Gauge("device_health_value_std", "Standard deviation of computed health metric", all_labels[:-1], registry=registry),
        "registry": registry
    }

def export_health(device, window, metric, status, category, job, stats=None, labels_extra=None):
    labels_extra = labels_extra or {}
    all_labels = {
        "device": device,
        "window": window,
        "metric": metric,
        "category": category,
        "job": job,
        "status": status,
        **labels_extra
    }

    gauges = get_health_gauges(list(labels_extra.keys()))
    gauges["status"].labels(**all_labels).set(1)

    if stats:
        base_labels = {k: v for k, v in all_labels.items() if k != "status"}
        gauges["mean"].labels(**base_labels).set(stats["mean"])
        gauges["max"].labels(**base_labels).set(stats["max"])
        gauges["min"].labels(**base_labels).set(stats["min"])
        gauges["std"].labels(**base_labels).set(stats["std"])

    push_to_gateway("http://localhost:9091", job=f"health_{job}", registry=gauges["registry"])