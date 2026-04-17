📌 Problem Statement

Design and implement an SDN-based system that monitors network utilization and enforces firewall rules. The system collects byte counters from switches, estimates bandwidth usage, displays utilization, and updates periodically.

🎯 Objective
Implement SDN using Mininet and POX controller
Apply firewall rules using OpenFlow
Monitor network traffic using byte counters
Estimate bandwidth usage
Display utilization and update periodically
🖥️ Topology
Hosts:
h1 → 10.0.0.1
h2 → 10.0.0.2
h3 → 10.0.0.3
Switch: s1
Controller: POX (port 6633)
🔒 Firewall Policy
h1 → h3 ❌ BLOCKED
h3 → h1 ❌ BLOCKED
h1 → h2 ✅ ALLOWED
h2 → h3 ✅ ALLOWED
⚙️ Setup and Execution
🖥️ Terminal 1 – Start POX Controller
cd ~/pox
python3 pox.py log.level --DEBUG forwarding.sdn_firewall
🖥️ Terminal 2 – Start Mininet Topology
cd ~/Desktop/sdn-project
sudo python3 topology.py
🧪 Testing
🔹 Connectivity Test
pingall
h1 ping h2
h1 ping h3
🔹 Bandwidth Test
h2 iperf -s &
h1 iperf -c 10.0.0.2 -t 5
📊 Network Utilization Monitoring
🔹 Byte Counters
sh ovs-ofctl dump-ports s1
🔹 Flow Table (Packet + Byte Count)
sh ovs-ofctl dump-flows s1
🔹 Periodic Monitoring (Real-Time)
sh watch -n 2 ovs-ofctl dump-ports s1
📈 Results
Ping Test: 33% packet loss (firewall rules applied)
Allowed Traffic: h1 ↔ h2 successful
Blocked Traffic: h1 ↔ h3 failed
Bandwidth: ~73 Gbps (iperf result)
Byte Counters: RX/TX bytes observed from switch
Monitoring: Real-time updates every 2 seconds
📸 Screenshots
Topology Initialization




Firewall Test




Bandwidth Test




Byte Counters




Periodic Monitoring




Flow Table




🎯 Conclusion

This project successfully demonstrates SDN-based firewall control and real-time network utilization monitoring. It uses OpenFlow rules to control traffic and switch statistics to measure bandwidth and performance.
