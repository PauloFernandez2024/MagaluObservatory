BITS_IN_MEGABIT = 1_000_000  # usado para converter Mbps para bps

########################################################################
#                  Seção de Definição das Fórmulas                     #
########################################################################

#
# Network session
#
def storage(row):
    return 100 * row['hrStorageUsed'] / row['hrStorageSize'] if row['hrStorageSize'] > 0 else 0

def bandwidth(row):
    return 8 * 100 * (row['ifHCInOctets'] + row['ifHCOutOctets']) / (row['ifHighSpeed'] * BITS_IN_MEGABIT * row['time_diff_seconds']) if row['ifHighSpeed'] > 0 else 0

def indiscards(row):
    total = row['ifHCInBroadcastPkts'] + row['ifHCInMulticastPkts'] + row['ifHCInUcastPkts']
    return (100 * row['ifInDiscards']) / total if total > 0 else 0

def outdiscards(row):
    total = row['ifHCOutBroadcastPkts'] + row['ifHCOutMulticastPkts'] + row['ifHCOutUcastPkts']
    return (100 * row['ifOutDiscards']) / total if total > 0 else 0

def inerrors(row):
    total = row['ifHCInBroadcastPkts'] + row['ifHCInMulticastPkts'] + row['ifHCInUcastPkts']
    return (100 * row['ifInErrors']) / total if total > 0 else 0

def outerrors(row):
    total = row['ifHCOutBroadcastPkts'] + row['ifHCOutMulticastPkts'] + row['ifHCOutUcastPkts']
    return (100 * row['ifOutErrors']) / total if total > 0 else 0


#
# BGP session
#
def bgp(row):
    score = 0
    # Estado estabelecido (peso: 40)
    if int(row.get("bgpPeerState", 0)) == 6:
        score += 40
    # Uptime (peso: 20)
    if float(row.get("bgpPeerFsmEstablishedTime", 0)) > 300:
        score += 20
    # Updates trocados (peso: 20)
    updates = int(row.get("bgpPeerInUpdates", 0)) + int(row.get("bgpPeerOutUpdates", 0))
    if updates > 10:
        score += 20
    # Mensagens totais trocadas (peso: 20)
    messages = int(row.get("bgpPeerInTotalMessages", 0)) + int(row.get("bgpPeerOutTotalMessages", 0))
    if messages > 50:
        score += 20
    return score

#
# Servers session
#
def cpu_load(row):
    return 100 * (1 - (row['node_cpu_seconds_total'] / row['time_diff_seconds'])) if row['time_diff_seconds'] > 0 else 0

def cpu_queue(row):
    return row['node_load1']

def io_load(row):
    return 100 * (row['node_cpu_seconds_total'] / row['time_diff_seconds']) if row['time_diff_seconds'] > 0 else 0

def io_queue(row):
    return row['node_disk_io_time_weighted_seconds_total'] / row['time_diff_seconds'] if row['time_diff_seconds'] > 0 else 0

def memory(row):
    used = row['node_memory_MemFree_bytes'] + row['node_memory_Buffers_bytes'] + row['node_memory_Cached_bytes']
    return 100 * (1 - (used / row['node_memory_MemTotal_bytes'])) if row['node_memory_MemTotal_bytes'] > 0 else 0

def memory_swapping(row):
    return 1e3 * (row['node_vmstat_pswpin'] + row['node_vmstat_pswpout']) / row['time_diff_seconds'] if row['time_diff_seconds'] > 0 else 0

def network_packets(row):
    return (row['node_network_receive_packets_total'] + row['node_network_transmit_packets_total']) / row['time_diff_seconds'] if row['time_diff_seconds'] > 0 else 0

def network_errors(row):
    return (row['node_network_receive_errs_total'] + row['node_network_transmit_errs_total']) / row['time_diff_seconds'] if row['time_diff_seconds'] > 0 else 0

def filesystem(row):
    return 100 * (1 - (row['node_filesystem_avail_bytes'] / row['node_filesystem_size_bytes'])) if row['node_filesystem_size_bytes'] > 0 else 0

def smartmon_temperature(row):
     return row['smartmon_airflow_temperature_cel_value']

def nvme_temperature(row):
    return row['nvme_temperature_celsius']


#
# Firewall session
#
def ethtool_load_ratio(row):
    total_rx = row.get("packets_rx", 0) + row.get("packets_tx", 0)
    return total_rx / row["time_diff_seconds"] if total_rx else 0

def tcp_udp_health(row):
    score = 100
    if row.get("tcp_orphan", 0) > 0:
        score -= 30
    if row.get("tcp_tw", 0) > 0:
        score -= 20
    if row.get("udp_mem", 0) > 0:
        score -= 10
    return score


def numa_health(row):
    hit = row.get("numa_hit", 0)
    miss = row.get("numa_miss", 0)
    return 100 * hit / (hit + miss) if (hit + miss) > 0 else 100


def cpu_freq(row):
    return 100 * row.get("cur_freq_khz", 0) / row.get("max_freq_khz", 1)

def process_fd_usage(row):
    return 100 * row.get("open_fds", 0) / row.get("max_fds", 1)


########################################################################
#                  Seção de Definição das Funções                      #
########################################################################
formula = {
    'storage': storage,
    'bandwidth': bandwidth,
    'indiscards': indiscards,
    'outdiscards': outdiscards,
    'inerrors': inerrors,
    'outerrors': outerrors,
    'bgp': bgp,
    'cpu_load': cpu_load,
    'cpu_queue': cpu_queue,
    'io_load': io_load,
    'io_queue': io_queue,
    'memory': memory,
    'memory_swapping': memory_swapping,
    'network_packets': network_packets,
    'network_errors': network_errors,
    'filesystem': filesystem,
    'smartmon_temperature': smartmon_temperature,
    'nvme_temperature': nvme_temperature
    'network_ethtool': ethtool_load_ratio,
    'tcp_udp': tcp_udp_health,
    'numa': numa_health,
    'cpu_freq': cpu_freq,
    'processes': process_fd_usage,
}
