def spawn_ball_data(update, frames, i):
    from rocketleaguereplayanalysis.parser.location import \
        parse_loc_update, parse_rot_spawn, parse_sleep_update

    if 'initialization' in update['value']['spawned'].keys():
        loc = parse_loc_update(update['value']['spawned']['initialization'])
        rot = parse_rot_spawn(update['value']['spawned']['initialization'])
        sleep = parse_sleep_update(update['value']['spawned']['initialization'])
        if loc:
            frames[i]['ball']['loc'].update(loc)
        if rot:
            frames[i]['ball']['rot'].update(rot)
        if sleep:
            frames[i]['ball']['sleep'] = sleep


def update_ball_data(update, frames, i):
    from rocketleaguereplayanalysis.parser.location import \
        parse_loc_update, parse_rot_update, parse_sleep_update

    if 'TAGame.Ball_TA:HitTeamNum' in update['name']:
        frames[i]['ball']['last_hit'] = update['value']['byte']
    if 'TAGame.RBActor_TA:ReplicatedRBState' in update['name']:
        loc = parse_loc_update(update)
        rot = parse_rot_update(update)
        sleep = parse_sleep_update(update)
        if loc:
            frames[i]['ball']['loc'].update(loc)
        if rot:
            frames[i]['ball']['rot'].update(rot)
        if sleep:
            frames[i]['ball']['sleep'] = sleep
