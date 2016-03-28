#!/usr/bin/env python

from multiprocessing import Process, Queue

from control import ap
from xplane import xplane

auto = ap.Ap()
auto.level_wing(True)
auto.pitch_angle(True)


class Config(object):
    pass


def ap_worker(queue):
    while True:
        att = queue.get()
        control_out = auto.update(att)
        queue.put(control_out)


if __name__ == '__main__':
    ap_queue = Queue()
    config = Config()
    config.udp_ip = "127.0.0.1"
    config.udp_port = 49010
    config.xp_port = 49000

    fc_proc = Process(target=ap_worker, args=(ap_queue,))
    fc_proc.start()

    client_proc = Process(target=xplane.run, args=(config, ap_queue))
    client_proc.start()
