
class Pid:

    def __init__(self, kp=0.0, ki=0.0, kd=0.0, minimum=-1.0, maximum=1.0):
        self.gains = (kp, ki, kd)

        self.minimum = minimum
        self.maximum = maximum

        self._prev_error = 0.0
        self._integral = 0.0

    def reset(self):
        self._prev_error = 0.0
        self._integral = 0.0

    def update(self, error, delta_t):
        self._integral = self._integral + (error * delta_t)

        action = (self.gains[0] * error) + \
                 (self.gains[1] * self._integral) + \
                 (self.gains[2] * (error - self._prev_error) / delta_t)

        self._prev_error = error
        return min(max(action, self.minimum), self.maximum)

    def __set_gains(self, gains):
        self.gains = gains
        self.reset()
