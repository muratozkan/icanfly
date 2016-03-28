from __future__ import absolute_import
import socket
from .parser import *
import asyncio


class XPUdpListener:
    def __init__(self, udp_ip, xp_port, ap_queue):
        self.udp_ip = udp_ip
        self.xp_port = xp_port
        self.ap_queue = ap_queue
        self.command_socket = None

    def connection_made(self, transport):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def datagram_received(self, data, addr):
        loc, att = parse_state(data)
        self.ap_queue.put(att)
        control_out = self.ap_queue.get()
        print(att, control_out)
        if control_out is not None:
            self.command_socket.sendto(from_input(control_out), (self.udp_ip, self.xp_port))


def run(config, ap_queue):
    xpc = XPUdpListener(config.udp_ip, config.xp_port, ap_queue)
    loop = asyncio.get_event_loop()
    client_coro = loop.create_datagram_endpoint(lambda: xpc, local_addr=(config.udp_ip, config.udp_port))
    loop.run_until_complete(client_coro)
    loop.run_forever()
