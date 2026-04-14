# SDN Mininet Firewall Project

## Problem Statement
SDN-based firewall using Mininet and POX controller that blocks traffic between specific hosts using OpenFlow rules.

## Topology
- 3 hosts: h1 (10.0.0.1), h2 (10.0.0.2), h3 (10.0.0.3)
- 1 switch: s1
- Controller: POX (port 6633)

## Firewall Policy
- h1 to h3 : BLOCKED
- h1 to h2 : ALLOWED
- h2 to h3 : ALLOWED

## Setup and Execution
Terminal 1 - Start POX controller
cd ~/pox
python3 pox.py log.level --DEBUG forwarding.sdn_firewall

Terminal 2 - Start Mininet topology
cd ~/Desktop/sdn-project
sudo python3 topology.py

## Test Results
- pingall: 33% dropped (2 out of 6 flows blocked)
- h1 ping h2: 0% packet loss (allowed)
- h1 ping h3: 100% packet loss (blocked)
- iperf h1 to h2: 73.5 Gbits/sec

## References
1. https://mininet.org/overview/
2. https://noxrepo.github.io/pox-doc/html/
3. https://github.com/noxrepo/pox
