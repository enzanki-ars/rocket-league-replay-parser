def parse_loc_update(update):
    returned_data = {}
    if 'location' in update:
        if 'x' in update['location']:
            returned_data['x'] = update['location']['x']
        if 'y' in update['location']:
            returned_data['y'] = update['location']['y']
        if 'z' in update['location']:
            returned_data['z'] = update['location']['z']

    return returned_data


def parse_rot_spawn(update):
    returned_data = {}

    if 'rotation' in update:
        if 'x' in update['rotation']:
            returned_data['x'] = update['location']['x'] / 65536
        if 'y' in update['rotation']:
            returned_data['y'] = update['location']['y'] / 65536
        if 'z' in update['rotation']:
            returned_data['z'] = update['location']['z'] / 65536

    return returned_data


def parse_rot_update(update):
    returned_data = {}
    if 'rotation' in update:
        if 'x' in update['rotation']:
            returned_data['x'] = update['location']['x']['value'] / 65536
        if 'y' in update['rotation']:
            returned_data['y'] = update['location']['y']['value'] / 65536
        if 'z' in update['rotation']:
            returned_data['z'] = update['location']['z']['value'] / 65536

    return returned_data


def parse_ang_vel_update(update):
    returned_data = {}
    if 'angular_velocity' in update:
        if 'x' in update['angular_velocity']:
            returned_data['x'] = update['angular_velocity']['x']
        if 'y' in update['angular_velocity']:
            returned_data['y'] = update['angular_velocity']['y']
        if 'z' in update['angular_velocity']:
            returned_data['z'] = update['angular_velocity']['z']

    return returned_data


def parse_lin_vel_update(update):
    returned_data = {}
    if 'linear_velocity' in update:
        if 'x' in update['linear_velocity']:
            returned_data['x'] = update['linear_velocity']['x']
        if 'y' in update['linear_velocity']:
            returned_data['y'] = update['linear_velocity']['y']
        if 'z' in update['linear_velocity']:
            returned_data['z'] = update['linear_velocity']['z']

    return returned_data


def parse_sleep_update(update):
    if 'sleeping' in update:
        return update['sleeping']
