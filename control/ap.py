import pid
import state


class Ap:

    def __init__(self):
        self._pid = pid.Pid(0.005, 0.01, 0.01)

    def level_wing(self, attitude, delta_t):
        roll = self._pid.update(0 - attitude.roll, delta_t)
        return state.Control(0, roll, 0)
