from prometheus_api_client import MetricRangeDataFrame
from datetime import datetime, timedelta
import logging
from prometheus_api_client import PrometheusConnect
from metrics_exporter import export_health
import requests
import pandas as pd
import numpy as np
import yaml
from formulas import formula  # importa dicionário de funções de cálculo
from time_windows import time_windows  # importa janelas de tempo de outro arquivo

prometheus_url = "http://localhost:9090"
prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

# --- Carregar métricas por categoria de arquivo externo ---
with open("metrics.yaml") as f:
    network = yaml.safe_load(f)

# --- Detectar nome real do label de índice ---
def get_index_label(label_keys):
    for key in label_keys:
        if "index" in key.lower() and key != "__name__":
            return key
    return None

# --- Classificar status com base em thresholds ---
def classify(value, thresholds):
    if value >= thresholds["critical"]:
        return "CRITICAL"
    elif value >= thresholds["warning"]:
        return "WARNING"
    return "OK"

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

# --- Analisar por categoria com fórmulas compostas ---
def analyze_metric(metric, thresholds, label_config, duration, window_label, category):
    now = datetime.utcnow()
    start = now - duration

    metrics = network.get(category)
    if not metrics:
        logging.warning(f"Categoria {category} desconhecida ou não definida")
        return

    dfs = {}
    for m in metrics:
        df = get_metric_df(m, label_config, start, now)
        if df is not None:
            dfs[m] = df

    if not dfs:
        logging.warning(f"Sem dados para métricas da categoria {category}")
        return

    # Detectar labels em comum para merge
    example_df = next(iter(dfs.values()))
    label_candidates = set(example_df.columns) - {"__name__"}
    index_label = get_index_label(label_candidates)
    label_cols = [col for col in ["instance", "job"] + ([index_label] if index_label else []) if col in example_df.columns]

    # Juntar os dataframes por label
    try:
        base = dfs[metrics[0]].copy()
        for m in metrics[1:]:
            if m in dfs:
                base = base.join(dfs[m], rsuffix=f"_{m}", how="outer")
    except Exception as e:
        logging.error(f"Erro ao combinar DataFrames: {e}")
        return

    # Renomear colunas duplicadas e padronizar
    base.columns = metrics[:len(base.columns)]

    calc_values = []
    devices = []

    for idx, row in base.iterrows():
        row_dict = row.to_dict()
        row_dict["time_diff_seconds"] = duration.total_seconds()
        if category == "storage" and row_dict.get("hrStorageDescr") != "Physical memory":
            continue

        try:
            value = formula[category](row_dict) if category in formula else row_dict[metrics[0]]
            calc_values.append(value)
            devices.append(idx[0] if isinstance(idx, tuple) else idx)
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

    status = classify(final_value, thresholds)
    device = devices[0] if devices else "unknown"

    export_health(
        device=device,
        window=window_label,
        metric=metric,
        status=status,
        category=category
    )

    logging.info(
        f"Health {metric} [{window_label}] @ {device}: {status} (mean={mean_val:.2f}, max={max_val:.2f}, min={min_val:.2f}, std={std_val:.2f})"
    )

# --- Execução automática por categoria e janela ---
with open("config.yaml") as f:
    config = yaml.safe_load(f)

thresholds_config = config["thresholds"]

# Exemplo genérico de label para todos
default_label_config = {"job": "network_switch_os10"}

for category, metric_list in network.items():
    for label, duration in time_windows.items():
        try:
            analyze_metric(
                metric=metric_list[0],
                thresholds=thresholds_config.get(category, {"warning": 80, "critical": 90}),
                label_config=default_label_config,
                duration=duration,
                window_label=label,
                category=category
            )
        except Exception as e:
            logging.error(f"Erro ao analisar {category} [{label}]: {e}")
