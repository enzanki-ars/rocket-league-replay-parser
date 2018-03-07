def get_field_dimensions(frames):
    ball_loc = {'x': [], 'y': []}

    for frame in frames:
        ball_loc['x'].append(frame['ball']['loc']['x'])
        ball_loc['y'].append(frame['ball']['loc']['y'])

    center_x = ball_loc['x'][0]
    center_y = ball_loc['y'][0]

    max_x = max(ball_loc['x'])
    min_x = min(ball_loc['x'])
    x_w = max(max_x - center_x, center_x - min_x) * 2

    max_y = max(ball_loc['y'])
    min_y = min(ball_loc['y'])
    y_w = max(max_y - center_y, center_y - min_y) * 2

    return {
        'center_x': center_x,
        'center_y': center_y,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
        'x_size': x_w,
        'y_size': y_w,
    }


def fix_pressure_possession_values(frames):
    for i, frame in enumerate(frames):
        max_pressure = (frames[i]['pressure'][0] +
                        frames[i]['pressure'][1])

        max_possession = (frames[i]['possession'][0] +
                          frames[i]['possession'][1])

        if max_pressure > 0:
            frames[i]['pressure'][0] = (frames[i]['pressure'][0] /
                                        max_pressure)
            frames[i]['pressure'][1] = (frames[i]['pressure'][1] /
                                        max_pressure)
        else:
            frames[i]['pressure'][0] = .5
            frames[i]['pressure'][1] = .5

        if max_possession > 0:
            frames[i]['possession'][0] = (
                    frames[i]['possession'][0] /
                    max_possession)
            frames[i]['possession'][1] = (
                    frames[i]['possession'][1] /
                    max_possession)
        else:
            frames[i]['possession'][0] = .5
            frames[i]['possession'][1] = .5


def parse_pressure(frames):
    from rocketleaguereplayanalysis.util.sync import \
        get_sync_delta_type

    field_dimensions = get_field_dimensions(frames)

    frames[0]['pressure'] = {0: 0, 1: 0}

    for i, frame in enumerate(frames):
        if frame['ball']['loc']['y'] > \
                field_dimensions['center_y']:

            frame['pressure'] = {
                0: (frames[i - 1]['pressure'][0] +
                    frame['time'][get_sync_delta_type()]),
                1: frames[i - 1]['pressure'][1]
            }

        elif frame['ball']['loc']['y'] < \
                field_dimensions['center_y']:
            frame['pressure'] = {
                0: frames[i - 1]['pressure'][0],
                1: (frames[i - 1]['pressure'][1] +
                    frame['time'][get_sync_delta_type()])
            }

        else:
            if i > 0:
                frame['pressure'] = {
                    0: frames[i - 1]['pressure'][0],
                    1: frames[i - 1]['pressure'][1]
                }
            else:
                frame['pressure'] = {
                    0: 0,
                    1: 0
                }


def parse_possession(frames):
    from rocketleaguereplayanalysis.util.sync import \
        get_sync_delta_type

    frames[0]['possession'] = {0: 0, 1: 0}

    for i, frame in enumerate(frames):
        if frame['ball']['last_hit'] == 0:
            frame['possession'] = {
                0: (frames[i - 1]['possession'][0] +
                    frame['time'][get_sync_delta_type()]),
                1: frames[i - 1]['possession'][1]}

        elif frame['ball']['last_hit'] == 1:
            frame['possession'] = {
                0: frames[i - 1]['possession'][0],
                1: (frames[i - 1]['possession'][1] +
                    frame['time'][get_sync_delta_type()])
            }
        else:
            if i > 0:
                frame['possession'] = {
                    0: frames[i - 1]['possession'][0],
                    1: frames[i - 1]['possession'][1]
                }
            else:
                frame['possession'] = {0: 0, 1: 0}


def parse_total_boost(frames, player_info):
    team0_mod = 0
    team1_mod = 1

    for player_id in player_info:
        if 'team' in player_info[player_id]:
            if player_info[player_id]['team'] == 0:
                team0_mod += 1
            elif player_info[player_id]['team'] == 1:
                team1_mod += 1

    for i, frame in enumerate(frames):
        frame['total_boost'] = {0: 0, 1: 0}
        for player_id in player_info:
            if 'team' in player_info[player_id] and \
                    player_info[player_id]['team']:
                frame['total_boost'][player_info[player_id]['team']] += \
                    frame['cars'][player_id]['boost']

        if team0_mod:
            frame['total_boost'][0] = frame['total_boost'][0] / team0_mod
        if team1_mod:
            frame['total_boost'][1] = frame['total_boost'][1] / team1_mod
