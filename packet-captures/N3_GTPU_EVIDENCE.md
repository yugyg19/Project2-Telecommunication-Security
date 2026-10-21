# N3/GTP-U Packet Evidence

Capture: `n3-gtpu.pcap`

Capture interface: `br-fe67497815b0`

Filter: `udp port 2152`

Result:
- 1,355 packets captured
- 1,371 packets received by filter
- 0 packets dropped

TShark decoded the packets as `GTP/TCP` and `GTP/iPerf3`.

Observed:
- Outer gNB IP: `172.22.0.23`
- Outer UPF IP: `172.22.0.8`
- UDP/2152
- UE inner IP: `192.168.100.2`
- iperf3 inner IP: `10.20.6.21`
- UE→UPF TEID: `0x0000b505`
- UPF→gNB TEID: `0x00000001`

Example hierarchy:

**Outer IP → UDP/2152 → GTP-U → Inner IP → TCP/UDP**
