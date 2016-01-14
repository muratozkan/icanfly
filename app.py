#!/usr/bin/env python

from control import state
from xplane import parser
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 49010

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print "received message:", parser.to_state(data)
    '''
    data_file = open("./test-vectors/11_17_19_20.bin")
    sample_data = data_file.read()
    print parser.to_state(sample_data)
    '''
