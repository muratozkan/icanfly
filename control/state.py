from collections import namedtuple

# These structures define the state of the craft, usually acquired through on-board sensors.

# lat, lon in degrees, alt (from mean sea level - msl) in meters
Location = namedtuple('Location', ['lat', 'lon', 'alt'])

# degrees, w.r.t. body frame
# For reference, see: https://en.wikipedia.org/wiki/Flight_dynamics_(fixed-wing_aircraft)
Attitude = namedtuple('Attitude', ['pitch', 'yaw', 'roll'])

# horizontal and vertical speed (in meters/second) w.r.t. Earth frame
Speed = namedtuple('Speed', ['h', 'v'])

# current throttle level, should be between 0 .. 1
Throttle = namedtuple('Throttle', ['all'])

# control inputs, should be -1 .. 1
Control = namedtuple('Control', ['elevator', 'aileron', 'rudder'])
