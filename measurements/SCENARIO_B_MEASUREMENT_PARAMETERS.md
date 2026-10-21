# Scenario B — Measurement Parameters and Procedure

## Complete measured user-plane path

UE `192.168.100.2` → UERANSIM gNB `172.22.0.23` → N3/GTP-U → Open5GS UPF
→ N6 `10.20.6.0/24` → application/performance service.

Application endpoints:
- Nginx: `10.20.6.20:80`
- iperf3: `10.20.6.21:5201`

## Recorded parameters

| Test | Parameter |
|---|---|
| ICMP | 20 packets/run, 3 runs |
| TCP | 10 seconds/run, 3 runs, iperf3 server 10.20.6.21:5201 |
| UDP | 10 Mbps offered, 10 seconds/run, 3 runs |
| HTTP | 10.20.6.20:80, 3 requests |
| Rate limitation | UPF N6 `eth1`, TBF 20 Mbit/s, burst 32 kbit, latency 400 ms |
| N3 capture | Docker bridge `br-fe67497815b0`, UDP/2152 |

## Important measured results

TCP baseline receiver: **296.3 Mbit/s** average.

TCP with N6 20 Mbit/s limit: **19.0 Mbit/s** average receiver.

Reduction: approximately **93.6%**.

ICMP average RTT: **2.287 ms**, with 0% loss.

UDP: **10.0 Mbit/s received**, **0.064 ms average jitter**, **0% loss**.

HTTP: **8.022 ms average total response**, 3/3 HTTP 200.

## N3 packet evidence

Capture:
`scenario-b/packet-captures/n3-gtpu.pcap`

- 1,355 packets captured
- 1,371 packets received by filter
- 0 packets dropped
- UDP/2152
- Outer gNB `172.22.0.23` ↔ UPF `172.22.0.8`
- Inner UE `192.168.100.2` ↔ iperf3 `10.20.6.21`
- TEID UE→UPF `0x0000b505`
- TEID UPF→gNB `0x00000001`

The TShark decode showed `GTP/TCP` and `GTP/iPerf3`, including the inner IP traffic.
