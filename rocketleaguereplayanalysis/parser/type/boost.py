def update_boost_data(update, frames, current_car_objects,
                      current_boost_objects, i):
    actor_id = update['Id']

    # Find updated boost values
    if 'TAGame.CarComponent_TA:Vehicle' in update:
        car_id = update['TAGame.CarComponent_TA:Vehicle']['ActorId']

        for player_id in current_boost_objects:
            if car_id == current_car_objects[player_id] and \
                    car_id not in current_boost_objects[player_id]:
                current_boost_objects[player_id].append(update['Id'])

    if 'TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount' in update:
        for player_id in current_boost_objects:
            if actor_id in current_boost_objects[player_id]:
                frames[i]['cars'][player_id]['boost'] = \
                    update['TAGame.CarComponent_Boost_TA:'
                           'ReplicatedBoostAmount'] / 255

    if 'TAGame.CarComponent_TA:Active' in update:
        for player_id in current_boost_objects:
            if actor_id in current_boost_objects[player_id]:
                frames[i]['cars'][player_id]['boosting'] = update[
                    'TAGame.CarComponent_TA:Active']


def deplete_boost(current_car_objects, frames, i, player_info,
                  real_replay_delta):
    for player_id in current_car_objects:
        if player_id in player_info and \
                frames[i]['cars'][player_id]['boosting']:
            frames[i]['cars'][player_id]['boost'] -= \
                real_replay_delta * 85 / 255
            frames[i]['cars'][player_id]['boost'] = \
                max(0, frames[i]['cars'][player_id]['boost'])
