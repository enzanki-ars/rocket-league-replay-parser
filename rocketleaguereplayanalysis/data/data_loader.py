def parse_data(data):
    from rocketleaguereplayanalysis.parser.frames import load_frames
    from rocketleaguereplayanalysis.util.extra_info import parse_pressure, \
        parse_possession, fix_pressure_possession_values, parse_total_boost

    frames = load_frames(data)

    parse_pressure(frames)
    parse_possession(frames)
    parse_total_boost(frames)

    fix_pressure_possession_values(frames)

    return frames
