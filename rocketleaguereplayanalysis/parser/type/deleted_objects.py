def parse_deleted_objects(current_ball_object, current_boost_objects,
                          current_car_objects, data, frames, i, player_info):
    # Check for deleted actors
    for actor_id in data['Frames'][i]['DeletedActorIds']:
        if actor_id == current_ball_object:
            frames[i]['ball'] = {'loc': {'x': 0, 'y': 0, 'z': 0},
                                 'rot': {'x': 0, 'y': 0, 'z': 0},
                                 'sleep': True,
                                 'last_hit': None}
        else:
            for player_id in current_boost_objects:
                if player_id in player_info and \
                        actor_id in current_boost_objects[player_id]:
                    current_boost_objects[player_id].remove(actor_id)
            for player_id in current_car_objects:
                if player_id in player_info and \
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
