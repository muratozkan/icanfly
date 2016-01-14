from control import state
import struct

DATA_FORMAT = "<I8f"
DATA_LEN = 36
DATA_OFFSET = 5

XPLANE_LOCATION_INDEX = 20
XPLANE_ATTITUDE_INDEX = 17


def to_state(data):
    parsed = parse_data(data)
    return to_location(parsed), to_attitude(parsed)


def parse_data(data):
    sliced = [data[x:x + DATA_LEN] for x in range(DATA_OFFSET, len(data), DATA_LEN)]
    parsed = [struct.unpack(DATA_FORMAT, x) for x in sliced]

    # Create a dictionary, keys -> first elements of each tuple; values -> remaining elements
    return dict(map(lambda t: (t[0], t[1:]), parsed))


def to_location(parsed_map):
    raw_location = get_raw_data(parsed_map, XPLANE_LOCATION_INDEX)
    if raw_location is None:
        return None

    return state.Location(raw_location[0], raw_location[1], to_meter(raw_location[2]))


def to_attitude(parsed_map):
    raw_attitude = get_raw_data(parsed_map, XPLANE_ATTITUDE_INDEX)
    if raw_attitude is None:
        return None

    return state.Attitude(raw_attitude[0], raw_attitude[2], raw_attitude[1])


def get_raw_data(parsed_map, index):
    if index in parsed_map:
        return parsed_map[index]
    return None


'''
    TODO: Find & use a module for unit conversions
'''
def to_meter(foot):
    return foot * .305
