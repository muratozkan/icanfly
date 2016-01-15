#!/usr/bin/env python

from control import state,ap
from xplane import parser
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 49010

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    auto = ap.Ap()

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        loc, att = parser.parse_state(data)
        control = auto.level_wing(att)
        print att
        print control
        sock.sendto(parser.from_input(control), (UDP_IP, 49000))
    '''
    data_file = open("./test-vectors/11_17_19_20.bin")
    sample_data = data_file.read()
    print parser.to_state(sample_data)
    '''
    '''
    control = state.Control(0.3, 0.5, 0.2)
    raw = parser.from_input(control)
    # raw= parser._to_raw_data(11, control.elevator, control.aileron, (control.rudder / 5))
    '''
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    control = state.Control(0.5, 0, 0)
    raw = parser.from_input(control)

    while True:
        time.sleep(0.2)
        sock.sendto(raw, (UDP_IP, 49000))
    '''
