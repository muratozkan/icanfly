from control import state
import struct

DATA_FORMAT = "<I8f"
DATA_HEADER_FORMAT = "<4cB"
DATA_LEN = 36
DATA_OFFSET = 5

XP_LOCATION_INDEX = 20
XP_ATTITUDE_INDEX = 17
XP_CONTROL_INDEX = 11


def parse_state(data):
    parsed = parse_raw(data)
    return _get_location(parsed), _get_attitude(parsed)


def parse_raw(data):
    sliced = [data[x:x + DATA_LEN] for x in range(DATA_OFFSET, len(data), DATA_LEN)]
    parsed = [struct.unpack(DATA_FORMAT, x) for x in sliced]

    # Create a dictionary, keys -> first elements of each tuple; values -> remaining elements
    return dict(map(lambda t: (t[0], t[1:]), parsed))


def from_input(control):
    header = struct.pack(DATA_HEADER_FORMAT, b"D", b"A", b"T", b"A", 0)
    # XPlane Rudder input is between 0 .. 0.2, so we scale down elevator input
    raw_data = _to_raw_data(XP_CONTROL_INDEX, control.elevator, control.aileron, (control.rudder / 5))
    data = struct.pack(DATA_FORMAT, *raw_data)
    return header + data


def _to_raw_data(index, *data_points):
    data_len = len(data_points)
    if data_len > 8:
        raise ValueError("tuple should have at most 8 values")
    return [index] + [data_points[x] if x < data_len else -999 for x in range(0, 8)]


def _get_location(parsed_map):
    raw_location = parsed_map.get(XP_LOCATION_INDEX, None)
    if raw_location is None:
        return None

    return state.Location(raw_location[0], raw_location[1],
                          _convert_meter(raw_location[2]),_convert_meter(raw_location[3]))


def _get_attitude(parsed_map):
    raw_attitude = parsed_map.get(XP_ATTITUDE_INDEX, None)
    if raw_attitude is None:
        return None

    return state.Attitude(raw_attitude[0], raw_attitude[2], raw_attitude[1])


'''
    TODO: Find & use a module for unit conversions
'''
def _convert_meter(foot):
    return foot * .305
