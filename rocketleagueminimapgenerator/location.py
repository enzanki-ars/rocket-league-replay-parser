def parse_loc_spawn(frame_data):
    spawn_data = (frame_data['value']['spawned_replication_value']
                  ['initialization'])

    returned_data = {}

    if 'location' in spawn_data:
        if 'x' in spawn_data['location']:
            returned_data['x'] = spawn_data['location']['x']
        if 'y' in spawn_data['location']:
            returned_data['y'] = spawn_data['location']['y']
        if 'z' in spawn_data['location']:
            returned_data['z'] = spawn_data['location']['z']

    return returned_data


def parse_rot_spawn(frame_data):
    spawn_data = (frame_data['value']['spawned_replication_value']
                  ['initialization'])

    returned_data = {}

    if 'rotation' in spawn_data:
        if 'x' in spawn_data['rotation']:
            returned_data['x'] = spawn_data['rotation']['x']
        if 'y' in spawn_data['rotation']:
            returned_data['y'] = spawn_data['rotation']['y']
        if 'z' in spawn_data['rotation']:
            returned_data['z'] = spawn_data['rotation']['z']

    return returned_data


def parse_loc_update(updated_data):
    update = updated_data['value']['rigid_body_state_attribute_value']

    returned_data = {}
    if 'location' in update:
        if 'x' in update['location']:
            returned_data['x'] = update['location']['x']
        if 'y' in update['location']:
            returned_data['y'] = update['location']['y']
        if 'z' in update['location']:
            returned_data['z'] = update['location']['z']

    return returned_data


def parse_rot_update(updated_data):
    update = updated_data['value']['rigid_body_state_attribute_value']

    returned_data = {}

    if 'rotation' in update:
        if 'x' in update['rotation']:
            returned_data['x'] = update['rotation']['x']['value'] / 65536 * 360
        if 'y' in update['rotation']:
            returned_data['y'] = update['rotation']['y']['value'] / 65536 * 360
        if 'z' in update['rotation']:
            returned_data['z'] = update['rotation']['z']['value'] / 65536 * 360

    return returned_data
