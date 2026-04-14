from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

class Firewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Firewall, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)

        if ip:
            src = ip.src
            dst = ip.dst

            # 🚫 BLOCK RULE
            if (src == "10.0.0.1" and dst == "10.0.0.3") or \
               (src == "10.0.0.3" and dst == "10.0.0.1"):
                self.logger.info(f"BLOCKED: {src} -> {dst}")
                return  # Drop packet

            # ✅ ALLOW others
            self.logger.info(f"ALLOWED: {src} -> {dst}")

        # Normal forwarding (flood)
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=msg.match['in_port'],
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)
