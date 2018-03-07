def parse_data(data):

    from rocketleaguereplayanalysis.data.actor_data import parse_actor_data
    from rocketleaguereplayanalysis.data.object_numbers import \
        parse_player_info, parse_game_event_num
    from rocketleaguereplayanalysis.parser.frames import load_frames
    from rocketleaguereplayanalysis.util.extra_info import parse_pressure, \
        parse_possession, fix_pressure_possession_values, parse_total_boost

    actor_data = parse_actor_data(data)
    player_info, team_info = parse_player_info(data)
    game_event_num = parse_game_event_num(actor_data)

    frames = load_frames(data, player_info, team_info, game_event_num)

    parse_pressure(frames)
    parse_possession(frames)
    parse_total_boost(frames, player_info)

    fix_pressure_possession_values(frames)

    return frames, actor_data, player_info, team_info, game_event_num
