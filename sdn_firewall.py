from pox.core import core
from pox.lib.addresses import IPAddr
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# --- FIREWALL RULES ---
# Block traffic from h1 (10.0.0.1) to h3 (10.0.0.3)
BLOCKED_PAIRS = [
    ("10.0.0.1", "10.0.0.3"),
    ("10.0.0.3", "10.0.0.1"),
]

class SDNFirewall(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}
        log.info("SDN Firewall Controller connected to %s" % connection)
        self._install_firewall_rules()

    def _install_firewall_rules(self):
        for src_ip, dst_ip in BLOCKED_PAIRS:
            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.match.dl_type = 0x0800  # IPv4
            msg.match.nw_src = IPAddr(src_ip)
            msg.match.nw_dst = IPAddr(dst_ip)
            # No actions = DROP
            self.connection.send(msg)
            log.info("Firewall rule installed: BLOCK %s -> %s" % (src_ip, dst_ip))

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        # Check if IP packet matches blocked pair
        ip = packet.find('ipv4')
        if ip:
            src = str(ip.srcip)
            dst = str(ip.dstip)
            for blocked_src, blocked_dst in BLOCKED_PAIRS:
                if src == blocked_src and dst == blocked_dst:
                    log.info("BLOCKED packet: %s -> %s" % (src, dst))
                    return  # Drop silently

        # MAC learning
        self.mac_to_port[packet.src] = event.port

        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            # Install flow rule
            msg = of.ofp_flow_mod()
            msg.priority = 10
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.data = event.ofp
            self.connection.send(msg)
            log.info("ALLOW flow installed: %s -> %s (port %d)" % (src if ip else packet.src, dst if ip else packet.dst, out_port))
        else:
            # Flood
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

class SDNFirewallLauncher(object):
    def __init__(self):
        core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
        log.info("SDN Firewall waiting for switch connections...")

    def _handle_ConnectionUp(self, event):
        SDNFirewall(event.connection)

def launch():
    core.registerNew(SDNFirewallLauncher)
