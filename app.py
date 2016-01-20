#!/usr/bin/env python
import socket

from control import ap
from xplane import parser
import asyncio

UDP_IP = "127.0.0.1"
UDP_PORT = 49010


class UdpClient:
    def __init__(self):
        auto = ap.Ap()
        auto.level_wing(True)
        auto.pitch_angle(True)
        self.auto = auto
        self.command_socket = None

    def connection_made(self, transport):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def datagram_received(self, data, addr):
        loc, att = parser.parse_state(data)
        control_out = self.auto.update(att)
        print(att, control_out)
        if control_out is not None:
            self.command_socket.sendto(parser.from_input(control_out), (UDP_IP, 49000))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client_coro = loop.create_datagram_endpoint(UdpClient, local_addr=(UDP_IP, UDP_PORT))
    loop.run_until_complete(client_coro)
    loop.run_forever()
