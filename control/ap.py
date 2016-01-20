import time
import operator
from functools import reduce

from control.pid import Pid
from control.state import Control


class Ap:

    """
        Initialize the PID values for the autopilot. We'll eventually want to implement auto-tune ability to learn
        these values. For now they are statically set and would be different for every plane.
    """
    def __init__(self):
        self._ap_table = dict()
        self._last_update = None

    def level_wing(self, enabled):
        self._init_pid('wing_level', enabled, Pid(0.008, 0.005, 0.0033, -0.4, 0.4),
                       lambda a: 0 - a.roll, lambda x: Control(0, x, 0))

    def pitch_angle(self, enabled):
        self._init_pid('pitch_angle', enabled, Pid(0.1, 0.01, 0.01, -0.5, 0.5),
                       lambda a: 0 - a.pitch, lambda x: Control(x, 0, 0))

    def update(self, attitude):
        delta_t = 0.00001       # a very small initial value, for the first iteration
        if self._last_update is not None:
            delta_t = time.time() - self._last_update
        self._last_update = time.time()

        if len(self._ap_table) == 0:
            return None

        controls = [r(p.update(t(attitude), delta_t)) for p, t, r in self._ap_table.values()]
        return Control(*reduce(lambda x, y: map(operator.add, x, y), controls))

    def reset(self):
        for k, p in self._ap_table:
            p[0].reset()
        self._last_update = None

    def _init_pid(self, key, enabled, pid, target_func, control_func):
        if enabled:
            self._ap_table[key] = (pid, target_func, control_func)
        else:
            self._ap_table[key] = None
