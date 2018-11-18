def load_frames(data):
    import copy
    from rocketleaguereplayanalysis.parser.type.ball import spawn_ball_data, \
        update_ball_data
    from rocketleaguereplayanalysis.parser.type.player import update_player_data
    from rocketleaguereplayanalysis.parser.type.car import update_car_data
    from rocketleaguereplayanalysis.parser.type.game import update_game_data

    current_game_event_num = None
    current_team_info = {}
    current_ball_object = None
    current_car_objects = {}
    current_boost_objects = {}
    current_player_info = []

    frames = [len(data['content']['body']['frames'])]
    frames[0] = {
        'time': {
            'replay_time': data['frames'][0]['Delta'],
            'server_time': data['frames'][0]['Time'],
            'game_time': 300,
            'game_minutes': int(300 / 60),
            'game_seconds': 300 % 60,
            'replay_delta': data['frames'][0]['Delta'],
            'server_delta': data['frames'][0]['Delta'],
            'real_replay_time': 0,
            'real_replay_delta': data['frames'][0]['Delta']
        },
        'scoreboard': {
            'team0': 0,
            'team1': 0
        },
        'ball': {'loc': {'x': 0, 'y': 0, 'z': 0},
                 'rot': {'x': 0, 'y': 0, 'z': 0},
                 'sleep': True,
                 'last_hit': None},
        'cars': {}
    }

    for i in range(0, len(frames)):

        if i > 0:
            frames.append(copy.deepcopy(frames[i - 1]))

            server_time = data['frames'][i]['time']
            replay_time = (frames[i - 1]['time']['replay_time'] +
                           data['frames'][i]['delta'])
            game_time = frames[i - 1]['time']['game_time']
            server_delta = (data['frames'][i]['time'] -
                            data['frames'][i - 1]['time'])
            replay_delta = data['frames'][i]['delta']
        else:
            server_time = data['frames'][0]['time']
            replay_time = data['frames'][0]['delta']
            game_time = 300
            server_delta = data['frames'][0]['delta']
            replay_delta = data['frames'][0]['delta']

        if replay_delta == 0:
            # There seems to have been a goal here.
            real_replay_delta = replay_delta
            real_replay_time = (frames[i]['time']['real_replay_time'] +
                                replay_delta)
        else:
            real_replay_delta = server_delta
            real_replay_time = (frames[i]['time']['real_replay_time'] +
                                server_delta)

        frames[i]['time'] = {
            'replay_time': replay_time,
            'server_time': server_time,
            'game_time': game_time,
            'game_minutes': int(game_time / 60),
            'game_seconds': game_time % 60,
            'replay_delta': replay_delta,
            'server_delta': server_delta,
            'real_replay_time': real_replay_time,
            'real_replay_delta': real_replay_delta
        }

        for update in data['frames'][i]['replications']:
            actor_id = update['actor_id']['value']

            if 'destroyed' in update['value'].keys():
                actor_id = update['actor_id']['value']

                if actor_id == current_ball_object:
                    frames[i]['ball'] = {'loc': {'x': 0, 'y': 0, 'z': 0},
                                         'rot': {'x': 0, 'y': 0, 'z': 0},
                                         'sleep': True,
                                         'last_hit': None}
                else:
                    for player_id in current_boost_objects:
                        if player_id in current_player_info and \
                                actor_id in current_boost_objects[player_id]:
                            current_boost_objects[player_id].remove(actor_id)
                    for player_id in current_car_objects:
                        if player_id in current_player_info and \
                                actor_id == current_car_objects[player_id]:
                            current_car_objects[player_id] = None
                            current_boost_objects[player_id] = []
                            frames[i]['cars'][player_id]['loc'] = \
                                {'x': None, 'y': None, 'z': None}
                            frames[i]['cars'][player_id]['rot'] = \
                                {'x': 0, 'y': 0, 'z': 0}
                            frames[i]['cars'][player_id]['ang_vel'] = \
                                {'x': 0, 'y': 0, 'z': 0}
                            frames[i]['cars'][player_id]['lin_vel'] = \
                                {'x': 0, 'y': 0, 'z': 0}
                            frames[i]['cars'][player_id]['throttle'] = 0
                            frames[i]['cars'][player_id]['steer'] = .5
                            frames[i]['cars'][player_id]['ping'] = 0
                            frames[i]['cars'][player_id]['boost'] = 85 / 255
                            frames[i]['cars'][player_id]['boosting'] = False
                            frames[i]['cars'][player_id]['sleep'] = True
                            frames[i]['cars'][player_id]['drift'] = False
                            frames[i]['cars'][player_id]['2nd_cam'] = False
                            frames[i]['cars'][player_id]['driving'] = False

            if 'spawned' in update['value']:
                # Update ball object number
                if 'TAGame.Ball_TA' in update['value']['spawned']['class_name']:
                    current_ball_object = actor_id
                    spawn_ball_data(update, frames, i)

                if 'TAGame.PRI_TA' in update['value']['spawned']['class_name']:
                    current_player_info.append(actor_id)
                    if actor_id not in current_car_objects:
                        current_car_objects[actor_id] = None
                    if actor_id not in current_boost_objects:
                        current_car_objects[actor_id] = {}

            if 'updated' in update['value']:
                for new_update in update['value']['updated']:
                    if 'Engine.Pawn:PlayerReplicationInfo' in \
                            new_update['name']:
                        player_id = new_update['value']['flagged_int']['int']
                        current_car_objects[player_id] = actor_id

                    # Find updated boost values
                    if 'TAGame.CarComponent_TA:Vehicle' in new_update['name']:
                        car_id = new_update['value']['flagged_int']['int']

                        for player_id in current_boost_objects:
                            if car_id == current_car_objects[player_id] and \
                                    car_id not in \
                                    current_boost_objects[player_id]:
                                current_boost_objects[player_id].append(
                                    actor_id)

                    if 'TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount' in \
                            new_update['name']:
                        for player_id in current_boost_objects:
                            if actor_id in current_boost_objects[player_id]:
                                frames[i]['cars'][player_id]['boost'] = \
                                    new_update['value']['byte'] / 255

                    if 'TAGame.CarComponent_TA:Active' in new_update['name']:
                        for player_id in current_boost_objects:
                            if actor_id in current_boost_objects[player_id]:
                                if new_update['value']['byte'] == 1:
                                    frames[i]['cars'][player_id][
                                        'boosting'] = True
                                else:
                                    frames[i]['cars'][player_id][
                                        'boosting'] = False

                    # Update ball data
                    if actor_id == current_ball_object:
                        update_ball_data(new_update, frames, i)
                    # Update player info
                    elif actor_id in current_player_info:
                        update_player_data(new_update, frames, i, actor_id)
                    # Update game data
                    elif actor_id == current_game_event_num:
                        update_game_data(new_update, frames, i)
                    # Update team 0 score
                    elif actor_id == current_team_info[0]['id']:
                        if 'Engine.TeamInfo:Score' in new_update:
                            frames[i]['scoreboard']['team0'] = \
                                new_update['value']['int']
                    # Update team 1 score
                    elif actor_id == current_team_info[1]['id']:
                        if 'Engine.TeamInfo:Score' in new_update:
                            frames[i]['scoreboard']['team1'] = \
                                new_update['value']['int']
                    else:
                        # update car data
                        for player_id in current_car_objects:
                            if player_id in current_player_info and \
                                    actor_id == current_car_objects[player_id]:
                                update_car_data(new_update, frames, i,
                                                player_id)

            # Deplete Boost
            for player_id in current_car_objects:
                if player_id in current_player_info and \
                        frames[i]['cars'][player_id]['boosting']:
                    frames[i]['cars'][player_id]['boost'] -= \
                        real_replay_delta * 85 / 255
                    frames[i]['cars'][player_id]['boost'] = \
                        max(0, frames[i]['cars'][player_id]['boost'])

    return frames
