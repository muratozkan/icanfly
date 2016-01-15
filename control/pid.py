
class Pid:

    def __init__(self, kp, ki, kd, minimum=-1.0, maximum=1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.minimum = minimum
        self.maximum = maximum

        self._prev_error = 0.0
        self._integral = 0.0

        self.reset()

    def reset(self):
        self._prev_error = 0.0
        self._integral = 0.0

    def update(self, error, delta_t):
        self._integral = self._integral + (error * delta_t)

        action = (self.kp * error) + (self.ki * self._integral) + (self.kd * (error - self._prev_error) / delta_t)

        self._prev_error = error
        return min(max(action, self.minimum), self.maximum)
