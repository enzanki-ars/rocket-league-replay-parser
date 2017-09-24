def parse_loc_spawn(frame_data):
    spawn_data = frame_data['value']['spawned_replication_value'] \
        ['initialization']
    if 'location' in spawn_data:

        return {'x': spawn_data['location']['x'],
                'y': spawn_data['location']['y'],
                'z': spawn_data['location']['z']}
    else:
        return None


def parse_loc_update(updated_data):
    update = updated_data['value']['rigid_body_state_attribute_value']
    if 'location' in update:
        return {'x': update['location']['x'],
                'y': update['location']['y'],
                'z': update['location']['z']}
    else:
        return None


def return_no_position():
    return {'x': None,
            'y': None,
            'z': None}
