def storage(row):
    return 100 * row['hrStorageUsed'] / row['hrStorageSize'] if row['hrStorageSize'] > 0 else 0

def bandwidth(row):
    return 8 * 100 * (row['ifHCInOctets'] + row['ifHCOutOctets']) / (row['ifHighSpeed'] * 1_000_000 * row['time_diff_seconds']) if row['ifHighSpeed'] > 0 else 0

def indiscards(row):
    total = row['ifHCInBroadcastPkts'] + row['ifHCInMulticastPkts'] + row['ifHCInUcastPkts']
    return (100 * row['ifInDiscards']) / total if total > 0 else 0

def outdiscards(row):
    total = row['ifHCOutBroadcastPkts'] + row['ifHCOutMulticastPkts'] + row['ifHCOutUcastPkts']
    return (100 * row['ifOutDiscards']) / total if total > 0 else 0

formula = {
    'storage': storage,
    'bandwidth': bandwidth,
    'indiscards': indiscards,
    'outdiscards': outdiscards,
}
