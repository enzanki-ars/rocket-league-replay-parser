frames = None


def get_frames():
    global frames
    return frames


def load_frames():
    global frames

    import copy

    from tqdm import tqdm

    from rocketleagueminimapgenerator.data import get_data, get_data_end
    from rocketleagueminimapgenerator.object_numbers import get_ball_obj_nums, \
        get_car_obj_nums, get_player_info
    from rocketleagueminimapgenerator.location import parse_loc_spawn, \
        parse_loc_update, return_no_position

    data = get_data()

    ball_objects = get_ball_obj_nums()
    car_objects = get_car_obj_nums()
    player_info = get_player_info()

    data_end = get_data_end()

    frames = [len(data['content']['frames'])]
    frames[0] = {'delta': data['content']['frames'][0]['delta'],
                 'ball': {'loc': {'x': 0, 'y': 0, 'z': 0}},
                 'cars': {}}

    for player_id in player_info.keys():
        frames[0]['cars'][player_id] = {
            'loc': {'x': -10000, 'y': -10000, 'z': -10000}}

    for i in tqdm(range(0, data_end), desc='Frames', ascii=True):

        if i > 0:
            frames.append(copy.deepcopy(frames[i - 1]))

        frames[i]['delta'] = data['content']['frames'][i]['delta']

        for frame_data in data['content']['frames'][i]['replications']:
            if frame_data['actor_id']['value'] in ball_objects:

                if 'spawned_replication_value' in frame_data['value'].keys():
                    loc = parse_loc_spawn(frame_data)
                    if loc:
                        frames[i]['ball']['loc'] = loc
                elif 'updated_replication_value' in frame_data['value'].keys():
                    for updated_data in \
                            frame_data['value']['updated_replication_value']:
                        if updated_data['name'] == \
                                'TAGame.RBActor_TA:ReplicatedRBState':
                            loc = parse_loc_update(updated_data)
                            if loc:
                                frames[i]['ball']['loc'] = loc
            if frame_data['actor_id']['value'] in car_objects:
                car_id = frame_data['actor_id']['value']
                player_id = car_objects[car_id]

                if 'spawned_replication_value' in frame_data['value'].keys():
                    loc = parse_loc_spawn(frame_data)
                    if loc:
                        frames[i]['cars'][player_id]['loc'] = loc
                elif 'updated_replication_value' in frame_data['value'].keys():
                    for updated_data in \
                            frame_data['value']['updated_replication_value']:
                        if updated_data['name'] == \
                                'TAGame.RBActor_TA:ReplicatedRBState':
                            loc = parse_loc_update(updated_data)
                            if loc:
                                frames[i]['cars'][player_id]['loc'] = loc
                elif 'destroyed_replication_value' in \
                        frame_data['value'].keys():
                    frames[i]['cars'][player_id]['loc'] = return_no_position()
