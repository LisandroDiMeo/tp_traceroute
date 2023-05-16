#!/usr/bin/sudo python3

from time import time

from scapy.all import *
from scapy.layers.inet import IP, ICMP

import argparse
import pandas as pd

responses = {}


def rtt_for_reachable_ttl(reachable_ttl, url, times=1):
    cumulative_rtt = 0.0
    probe = IP(dst=url, ttl=reachable_ttl) / ICMP()
    ip = ''
    for t in range(0, times):
        t_i = time.time()
        ans = sr1(probe, verbose=False, timeout=0.8)
        if ans is not None:
            ip = ans.src
        t_f = time.time()
        rtt = (t_f - t_i) * 1000
        cumulative_rtt += rtt
    responses[url] = f"Mean RTT to {url} is {cumulative_rtt / times} with ttl of {reachable_ttl}, and with last ip of {ip}"
    return cumulative_rtt / times


def traceroute(url, max_ttl, ttl_burst=1):
    rtt_from_hops = {}
    prev_ip = None
    prev_rtt = 0
    reachable_ttl_found = False
    for ttl in range(1, max_ttl):
        print("\n\n")
        cumulative_rtt = 0.0
        instant_rtt_count = 0
        ip = ''
        for b in range(0, ttl_burst):
            packet = IP(dst=url, ttl=ttl) / ICMP()
            t_i = time.time()
            ans = sr1(packet, verbose=False, timeout=0.8)
            t_f = time.time()
            rtt = (t_f - t_i) * 1000
            print(f"total rtt: {rtt}")
            if ans is not None:
                ip = ans.src
                print(f"---- ttl: {ttl} | burst: {b} | ip_src: {ip} -----")
                if ans.type == 11 and ans.code == 0:  # Type 11 == Time Exceeded
                    print("=== Time Exceeded ===")
                    rtt_of_hop = rtt - prev_rtt
                    if prev_ip is not None:
                        print(f"{prev_ip} to {ip} had rtt of {rtt_of_hop}")
                    if rtt_of_hop <= 0.0:
                        instant_rtt_count += 1
                    else:
                        cumulative_rtt += rtt_of_hop
                elif ans.type is not None and ans.type == 0:  # Echo reply
                    print("=== Echo Reply ===")
                    reachable_ttl_found = True
                    rtt_of_hop = rtt - prev_rtt
                    if rtt_of_hop <= 0.0:
                        instant_rtt_count += 1
                    else:
                        cumulative_rtt += rtt_of_hop
            else:
                print(f"No answer for {packet} with ttl {ttl} burst nÂ° {b}.")
        print(f"---- end burst for ttl : {ttl} -----")
        if ip != '':
            prev_ip = ip
            mean_rtt = cumulative_rtt / max((ttl_burst - instant_rtt_count), 1)
            result = {
                "ip": ip,
                "mean_rtt": mean_rtt,
                "ttl": ttl,
                "target": url
            }
            rtt_from_hops[ip] = result
            prev_rtt = mean_rtt
        if reachable_ttl_found:
            print("\n\n Packet arrived to dst")
            rtt_for_reachable_ttl(ttl, url, ttl_burst)
            break
    return rtt_from_hops


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parser for traceroute")
    parser.add_argument('--ip', help="IPs To traceroute. Separated by commas")
    parser.add_argument('--ttl', help="Max TTL to try")
    parser.add_argument('--burst', help="Attempts for each ttl, this helps to calculate the mean RTT.")
    args = parser.parse_args()

    # Validate Arguments
    if args.ip is None or len(args.ip) == 0:
        print("Provide an IP!")
        exit(1)
    if args.ttl is None or int(args.ttl) <= 0:
        print("Invalid amount of ttl. Should be greater than 0, e.g: 1")
        exit(1)
    if args.burst is None or int(args.burst) <= 0:
        print("Invalid amount of ttl. Should be greater than 0, e.g: 1")
    ips_to_trace = args.ip.split(",")
    ttl_burst = int(args.burst)
    max_ttl = int(args.ttl)
    traceroute_dict = {}
    for ip_to_trace in ips_to_trace:
        print(f"Starting traceroute for {ip_to_trace} with TTL of {max_ttl} and burst of {ttl_burst}...")
        traceroute_dict[ip_to_trace] = traceroute(ip_to_trace, max_ttl, ttl_burst)

    # Parse output to CSV
    dataFrameDict = {
        "ip": [],
        "ttl": [],
        "mean_rtt": [],
        "target": []
    }
    for ip, traceroute_result in traceroute_dict.items():
        for ip_from_trace in traceroute_result.keys():
            dataFrameDict["ip"].append(traceroute_result[ip_from_trace]["ip"])
            dataFrameDict["ttl"].append(traceroute_result[ip_from_trace]["ttl"])
            dataFrameDict["mean_rtt"].append(traceroute_result[ip_from_trace]["mean_rtt"])
            dataFrameDict["target"].append(traceroute_result[ip_from_trace]["target"])
    df = pd.DataFrame(dataFrameDict)
    print("==================== Final Traceroute Result ====================")
    print(df)
    print("=================================================================")
    df.to_csv('output.csv', index=False)
