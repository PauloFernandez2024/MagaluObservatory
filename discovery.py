from prometheus_api_client import MetricRangeDataFrame
from datetime import datetime, timedelta
import logging
from prometheus_api_client import PrometheusConnect
from metrics_exporter import export_health
import requests
import pandas as pd
import numpy as np
import yaml
import time
import os
import json
from formulas import formula  # importa dicionário de funções de cálculo
from time_windows import time_windows  # importa janelas de tempo de outro arquivo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("discovery.log"),
        logging.StreamHandler()
    ]
)

BITS_IN_MEGABIT = 1_000_000
STATE_FILE = "window_exec_state.json"

prometheus_url = "http://localhost:9090"
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

# --- Carregar métricas por categoria de arquivo externo ---
with open("metrics.yaml") as f:
    categories = yaml.safe_load(f)

# --- Carregar lista de jobs dinamicamente com categorias permitidas ---
with open("jobs.yaml") as f:
    jobs_yaml = yaml.safe_load(f)
jobs_list = jobs_yaml.get("jobs", [])

# --- Detectar nome real do label de índice ---
def get_index_label(label_keys):
    for key in label_keys:
        if "index" in key.lower() and key != "__name__":
            return key
    return None

# --- Classificar status com base em thresholds ---
def classify(value, thresholds, category=None):
    positives = score_direction.get("positive", [])
    negatives = score_direction.get("negative", [])
    
    if category in positives:
        if value < thresholds["critical"]:
            return "CRITICAL"
        elif value < thresholds["warning"]:
            return "WARNING"
        return "OK"
    elif category in negatives:
        if value >= thresholds["critical"]:
            return "CRITICAL"
        elif value >= thresholds["warning"]:
            return "WARNING"
        return "OK"
    else:
        return "UNKNOWN"

# --- Obter DataFrame de uma métrica ---
def get_metric_df(metric, label_config, start, end):
    try:
        data = prom.get_metric_range_data(metric_name=metric, label_config=label_config, start_time=start, end_time=end)
        df = MetricRangeDataFrame(data)
        if df.empty:
            return None
        return df
    except Exception as e:
        logging.warning(f"Erro ao obter dados da métrica {metric}: {e}")
        return None

# --- Verificar se é hora de executar uma janela ---
def should_run(window, interval):
    now = datetime.utcnow()
    state = {}

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                state = json.load(f)
            except Exception:
                state = {}

    last_run_str = state.get(window)
    if last_run_str:
        try:
            last_run = datetime.fromisoformat(last_run_str)
            if now - last_run < interval:
                return False
        except Exception:
            pass

    state[window] = now.isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    return True


def extract_labels_from_index(idx, label_cols):
    """
    Retorna um dicionário {label: valor} com base nos rótulos do índice.
    """
    if isinstance(idx, tuple):
        return dict(zip(label_cols, idx))
    elif isinstance(idx, str) and len(label_cols) == 1:
        return {label_cols[0]: idx}
    return {}


# --- Analisar por categoria com fórmulas compostas ---
def analyze_metric(metric, thresholds, label_config, duration, window_label, category, metrics_cache):
    now = datetime.utcnow()
    start = now - duration

    metrics = categories.get(category)
    if not metrics:
        logging.warning(f"Categoria {category} desconhecida ou não definida")
        return

    dfs = {}
    for m in metrics:
        if m not in metrics_cache:
            df = get_metric_df(m, label_config, start, now)
            if df is not None:
                metrics_cache[m] = df
        if m in metrics_cache:
            dfs[m] = metrics_cache[m]

    if not dfs:
        logging.warning(f"Sem dados para métricas da categoria {category}")
        return

    example_df = next(iter(dfs.values()))
    label_candidates = set(example_df.columns) - {"__name__"}
    index_label = get_index_label(label_candidates)
    label_cols = [col for col in ["instance", "job"] + ([index_label] if index_label else []) if col in example_df.columns]

    try:
        base = dfs[metrics[0]].copy()
        for m in metrics[1:]:
            if m in dfs:
                base = base.join(dfs[m], rsuffix=f"_{m}", how="outer")
    except Exception as e:
        logging.error(f"Erro ao combinar DataFrames: {e}")
        return

    base.columns = metrics[:len(base.columns)]

    calc_values = []
    devices = []

    for idx, row in base.iterrows():
        row_dict = row.to_dict()
        row_dict["time_diff_seconds"] = duration.total_seconds()
        if category == "storage" and row_dict.get("hrStorageDescr") != "Physical memory":
            continue

        label_values = extract_labels_from_index(idx, label_cols)
        device = label_values.get("instance") or label_values.get("device") or "unknown"

        try:
            value = formula[category](row_dict) if category in formula else row_dict[metrics[0]]
            calc_values.append(value)
            devices.append(device)
        except Exception as e:
            logging.warning(f"Erro ao aplicar fórmula para {category} em {idx}: {e}")

    if not calc_values:
        logging.warning(f"Sem valores calculados para {category}")
        return

    mean_val = np.mean(calc_values)
    max_val = np.max(calc_values)
    min_val = np.min(calc_values)
    std_val = np.std(calc_values)
    final_value = mean_val

    status = classify(final_value, thresholds, category)
    device = devices[0] if devices else "unknown"

    export_health(
        device=device,
        window=window_label,
        metric=metric,
        status=status,
        category=category,
        job=label_config.get("job", "unknown"),
        stats={
            "mean": mean_val,
            "max": max_val,
            "min": min_val,
            "std": std_val
        }
    )

    logging.info(
        f"Health {metric} [{window_label}] @ {device}: {status} (mean={mean_val:.2f}, max={max_val:.2f}, min={min_val:.2f}, std={std_val:.2f})"
    )



def get_instances_for_job(prometheus_url, job_name):
    try:
        resp = requests.get(
            f"{prometheus_url}/api/v1/series",
            params={"match[]": f'up{{job="{job_name}"}}'}
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return sorted({item["instance"] for item in data if "instance" in item})
    except Exception as e:
        logging.error(f"Erro ao buscar instâncias para job '{job_name}': {e}")
        return []


# --- Execução contínua ---
with open("config.yaml") as f:
    config = yaml.safe_load(f)

thresholds_config = config["thresholds"]
score_direction = config.get("score_direction", {})

while True:
    for job_entry in jobs_list:
        job_name = job_entry["name"]
        allowed_categories = job_entry.get("categories", [])
        instances = get_instances_for_job(prometheus_url, job_name)
        if not instances:
            logging.warning(f"Nenhuma instância encontrada para job {job_name}")
            continue
        for instance in instances:
            label_config = {"job": job_name, "instance": instance}
            metrics_cache = {}
            for category in allowed_categories:
                metric_list = categories.get(category, [])
                for label, duration in time_windows.items():
                    if not should_run(label, duration):
                        continue
                    try:
                        analyze_metric(
                            metric=metric_list[0],
                            thresholds=thresholds_config.get(category, {"warning": 80, "critical": 90}),
                            label_config=label_config,
                            duration=duration,
                            window_label=label,
                            category=category,
                            metrics_cache=metrics_cache
                        )
                    except Exception as e:
                        logging.error(f"Erro ao analisar {category} [{label}] para job {job_name}: {e}")

    time.sleep(300)  # Aguarda 5 minutos antes do próximo ciclo
