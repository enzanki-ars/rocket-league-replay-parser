def update_car_data(update, frames, i, player_id):
    from rocketleaguereplayanalysis.parser.location import \
        parse_loc_update, parse_rot_update, \
        parse_sleep_update, parse_lin_vel_update, parse_ang_vel_update

    if 'TAGame.RBActor_TA:ReplicatedRBState' in update.keys():
        loc = parse_loc_update(update)
        rot = parse_rot_update(update)
        ang_vel = parse_ang_vel_update(update)
        lin_vel = parse_lin_vel_update(update)
        sleep = parse_sleep_update(update)

        if loc:
            frames[i]['cars'][player_id]['loc'].update(loc)
        if rot:
            frames[i]['cars'][player_id]['rot'].update(rot)
        if ang_vel:
            frames[i]['cars'][player_id]['ang_vel'].update(ang_vel)
        if lin_vel:
            frames[i]['cars'][player_id]['lin_vel'].update(lin_vel)
        if sleep:
            frames[i]['cars'][player_id]['sleep'] = sleep
    if 'TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount' in update.keys():
        frames[i]['cars'][player_id]['boost'] = \
            update['TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount'] / 255
    if 'TAGame.Vehicle_TA:ReplicatedThrottle' in update.keys():
        frames[i]['cars'][player_id]['throttle'] = \
            (update['TAGame.Vehicle_TA:ReplicatedThrottle'] / 255) * 2 - 1
    if 'TAGame.Vehicle_TA:ReplicatedSteer' in update.keys():
        frames[i]['cars'][player_id]['steer'] = \
            update['TAGame.Vehicle_TA:ReplicatedSteer'] / 255
    if 'TAGame.Vehicle_TA:bReplicatedHandbrake' in update.keys():
        # print('drift')
        frames[i]['cars'][player_id]['drift'] = \
            update['TAGame.Vehicle_TA:bReplicatedHandbrake']
    if 'TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera' in update.keys():
        print('2nd_cam')
        frames[i]['cars'][player_id]['2nd_cam'] = \
            update['TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera']
    if 'TAGame.Vehicle_TA:bDriving' in update.keys():
        # print('driving')
        frames[i]['cars'][player_id]['driving'] = \
            update['TAGame.Vehicle_TA:bDriving']
