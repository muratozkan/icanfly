import pid
import state
import time
import operator


class Ap:

    """
        Initialize the PID values for the autopilot. We'll eventually want to implement auto-tune ability to learn
        these values. For now they are statically set and would be different for every plane.
    """
    def __init__(self):
        self._ap_table = dict()
        self._last_update = None

    def level_wing(self, enabled):
        self._init_pid('wing_level', enabled, pid.Pid(0.005, 0.01, 0.01), lambda a: 0 - a.roll, lambda x: state.Control(0, x, 0))

    def pitch_angle(self, enabled):
        self._init_pid('pitch_angle', enabled, pid.Pid(1, 1, 1), lambda a: 0 - a.pitch, lambda x: state.Control(x, 0, 0))

    def update(self, attitude):
        delta_t = 0.00001       # a very small initial value, for the first iteration
        if self._last_update is not None:
            delta_t = time.time() - self._last_update
        self._last_update = time.time()

        if len(self._ap_table) == 0:
            return None

        controls = map(lambda (k, p): p[2](p[0].update(p[1](attitude), delta_t)), self._ap_table.items())
        return state.Control(*reduce(lambda x, y: map(operator.add, x, y), controls))

    def reset(self):
        for k, p in self._ap_table:
            p[0].reset()
        self._last_update = None

    def _init_pid(self, key, enabled, pid, target_func, control_func):
        if enabled:
            self._ap_table[key] = (pid, target_func, control_func)
        else:
            self._ap_table[key] = None
