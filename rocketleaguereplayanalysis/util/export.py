def get_all_data(frames, player_info, team_info):
    from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions
    return {
        'team_info': team_info,
        'player_info': player_info,
        'field_size': get_field_dimensions(frames),
        'frames': frames
    }


def export_parsed_data_json(video_prefix, frames, player_info, team_info):
    import json
    import os

    with open(os.path.join(video_prefix + '-export-parsed-data.json'),
              'w') as export_file:
        json.dump(get_all_data(frames, player_info, team_info), export_file)


def flatten(d, parent_key='', sep='_'):
    import collections

    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def export_parsed_data_csv(video_prefix, frames, player_info, team_info):
    import csv
    import os

    all_data = get_all_data(frames, player_info, team_info)

    with open(os.path.join(video_prefix + '-export-parsed-data.csv'),
              'w', newline='') as csvfile:
        fieldnames = flatten(all_data['frames'][0]).keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                dialect='excel')

        writer.writeheader()
        for frame in all_data['frames']:
            writer.writerow(flatten(frame))
