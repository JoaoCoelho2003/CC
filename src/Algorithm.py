from DNS import *

WEIGHT_RTT = 0.5
WEIGHT_PACKETLOSS = 0.5

# calculate_load: calculate load of an ip. Bigger means slower
def calculate_load (info_ip, max_rtt):
    Rtt = (info_ip[0] / info_ip[1]) / max_rtt
    PacketLoss = 1 - info_ip[2] / info_ip[1]
    return (Rtt * WEIGHT_RTT) + (PacketLoss * WEIGHT_PACKETLOSS)

# ratio_bettewen_nodes: obtain rate between the slower and the faster node
def ratio_bettewen_nodes (load1, load2):
    slower = load1 if load1 > load2 else load2
    faster = load1 if load1 < load2 else load2
    return slower / faster

# best_chunk_distribution: return best ip to send the chunk. 
def best_chunk_distribution (result, ips, info_nodes, max_rtt):
    current_ip = ips[0]
    info_ip = info_nodes.get(current_ip)
    current_load = calculate_load(info_ip, max_rtt)
    for ip in ips[1:]:
        info_ip = info_nodes.get(ip)
        load = calculate_load(info_ip, max_rtt)
        length_current_ip = len(result.get(current_ip))
        length_ip = len(result.get(ip))
        # if ip is slower than current and have more chunks, ignore it
        if load > current_load and length_ip > length_current_ip:
            continue
        # if ip is faster than current and have less chunks, send the chunk to it
        if load <= current_load and length_ip < length_current_ip:
            current_ip = ip
            current_load = load
        else:
            # if ip is slower and have less chunks, check if the sending the chunk to it compensates the load comparing the ratio between the loads and the number of chunks
            ratio = ratio_bettewen_nodes(load, current_load)
            comparator = (length_ip + 1) * ratio
            if comparator < length_current_ip:
                current_ip = ip
                current_load = load
    return current_ip

# best_ip_not_used: return best ip to send the chunk. If all ips are new, MSS_SEND = 0, return the first one
def best_ip_not_used (ips, info_nodes, max_rtt):
    best_ip = ips[0]
    info_ip = info_nodes.get(best_ip)
    best_load = calculate_load(info_ip, max_rtt) if info_ip[1] != 0 else 2
    for ip in ips[1:]:
        info_ip = info_nodes.get(ip)
        # If MSS_SEND is 0 dont send to this ip because it is already in the process of receiving a chunk
        if info_ip[1] != 0:
            load = calculate_load(info_ip, max_rtt)
            # if ip is faster than current, send the chunk to it
            if load < best_load and load != 0:
                best_load = load
                best_ip = ip
    return best_ip

# check_repeated: check for ips that its not being used by any other chunk
def check_repeated (result, ips):
    ips_not_used = []
    for ip in ips:
        if ip not in result:
            ips_not_used.append(ip)
    return ips_not_used 

# check for ips that are unknown 
def check_for_unknown (ips, info_nodes):
    for ip in ips:
        if info_nodes.get(ip) == None:
            return ip
    return None

# get_ip_with_less_chunks: return the ip with less chunks in result
def get_ip_with_less_chunks (result, ips):  
    best_ip = ips[0]
    best_chunks = len(result.get(best_ip))
    # search for the ip with less chunks in result to send the chunk
    for ip in ips[1:]:
        chunks = len(result.get(ip))
        if chunks < best_chunks:
            best_chunks = chunks
            best_ip = ip
    return best_ip

# choose_ip: choose the best ip to send the chunk
def choose_ip (result, ips, info_nodes, max_rtt):
    ip = None
    ips_not_used = check_repeated(result, ips)
    # if there is an ip not used, send the chunk to it
    if ips_not_used:
        ip = best_ip_not_used(ips_not_used, info_nodes, max_rtt)
        result[ip] = []
    else:
        # filter ips that are not new
        ips_not_new = [ip for ip in ips if info_nodes.get(ip)[1] != 0]
        if ips_not_new:
            ip = best_chunk_distribution(result,ips_not_new, info_nodes, max_rtt)
        # if all ips are new, send the chunk to the one with less chunks
        else:
            ip = get_ip_with_less_chunks(result, ips)
    return ip

# search_chunks: search the best nodes to send the chunks
def search_chunks (chunks_ips, info_nodes, max_rtt):
    # result is a dict (ips,[chunks])... each chunk appears only once
    result = {}
    for chunk, ips in chunks_ips.items():
        # if exists an ip unknown, send the chunk to it and create a new entry in info_nodes
        ip_unknown = check_for_unknown(ips, info_nodes)
        if ip_unknown:
            result[ip_unknown] = [chunk]
            info_nodes[ip_unknown] = [0,0,0, getIpByHostname(ip_unknown)]
        # if there is no ip unknown, choose the best ip to send the chunk
        else:
            ip = choose_ip(result, ips, info_nodes, max_rtt)
            result[ip].append(chunk)
    return result 
