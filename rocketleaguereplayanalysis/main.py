import argparse
import json
import os
from datetime import datetime

from rocketleaguereplayanalysis.data.data_loader import parse_data
from rocketleaguereplayanalysis.render.do_render import render
from rocketleaguereplayanalysis.util.asset_loc import get_assets_path
from rocketleaguereplayanalysis.util.data_explorer import data_explorer_cli
from rocketleaguereplayanalysis.util.export import export_parsed_data_json, \
    export_parsed_data_csv
from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions
from rocketleaguereplayanalysis.util.sync import set_sync_delta_type, \
    set_sync_time_type

version = 'v1.4.0-alpha3'

frame_num_format = '{0:05d}'


def main():
    parser = argparse.ArgumentParser(prog='rocketleaguereplayanalysis')

    # Required args
    parser.add_argument('game_json',
                        help='The name of the game json. '
                             'This can be a folder.',
                        nargs='+')

    assets_path, available_assets = get_assets_path()

    parser.add_argument('--render',
                        choices=available_assets,
                        nargs='+',
                        help='Select which renders are created. '
                             'Multiple renders can be separated by a space.')
    parser.add_argument('--render_all',
                        help='Render all possible videos.',
                        action='store_true')

    parser.add_argument('--data_explorer',
                        help='Explore the given data.',
                        action='store_true')
    parser.add_argument('--export_parsed_data_json',
                        help='Export the parsed data as JSON.',
                        action='store_true')
    parser.add_argument('--export_parsed_data_csv',
                        help='Export the parsed data as CSV.',
                        action='store_true')
    parser.add_argument('--show_field_size',
                        help='Show the calculated field size.',
                        action='store_true')
    parser.add_argument('--sync_to_live_recording',
                        help='Instead of syncing to a recording of the '
                             'in-game replay, sync to a recording of the '
                             'game played live.  In other words, if you have '
                             'recorded the game as you were playing it, set '
                             'this argument to sync to that recording. If '
                             'you recorded the replay after the game ended, '
                             'do not add this argument to sync to that '
                             'recording.',
                        action='store_true')
    parser.add_argument('--version',
                        action='version',
                        help='Print version and exit (' + version + ')',
                        version='%(prog)s ' + version)

    args = parser.parse_args()

    if args.sync_to_live_recording:
        set_sync_delta_type('server_delta')
        set_sync_time_type('server_time')
    else:
        set_sync_delta_type('real_replay_delta')
        set_sync_time_type('real_replay_time')

    replays_to_parse = []

    for game_json in args.game_json:
        if os.path.isdir(game_json):
            for file in os.listdir(game_json):
                if file.endswith('.json'):
                    replays_to_parse.append(os.path.join(game_json, file))

                    print(os.path.join(game_json, file),
                          'does not end with .json. '
                          'File was not added.')
        elif os.path.isfile(game_json):
            if game_json.endswith('.json'):
                replays_to_parse.append(game_json)
            else:
                print(game_json, 'does not end with .json. '
                                 'File was not added.')
        else:
            print(game_json, 'was not added as it does not '
                             'seem to be a file or directory.')

    for replay in replays_to_parse:

        out_prefix = os.path.basename(replay)

        game_name = out_prefix.split('.')[0]

        video_prefix = os.path.join('renders', game_name)

        print('=====', game_name, '=====')

        print('Loading data...')
        with open(replay) as data_file:
            data = json.load(data_file)
        print('Data successfully loaded.')

        print('In-Game Replay Name:', data['Properties']['ReplayName'])
        print('Date:', datetime.strptime(data['Properties']['Date'],
                                         '%Y-%m-%d %H-%M-%S'))

        print('Parsing data...')
        frames = parse_data(data)
        print('Data successfully parsed.')

        if not args.render and not args.render_all \
                and not args.data_explorer \
                and not args.show_field_size \
                and not args.export_parsed_data_json \
                and not args.export_parsed_data_csv:
            print('No action selected. Exiting. (See --help for more info '
                  'if you expected a video renders or the ability to easily '
                  'explore the data.)')
        else:
            if args.show_field_size:
                field_dimensions = get_field_dimensions(frames)
                print('Field Name:', data['Properties']['MapName'])
                print('Center X:  ', field_dimensions['center_x'])
                print('Center Y:  ', field_dimensions['center_y'])
                print('Max X:     ', field_dimensions['max_x'])
                print('Max Y:     ', field_dimensions['max_y'])
                print('Min X:     ', field_dimensions['min_x'])
                print('Min Y:     ', field_dimensions['min_y'])
                print('X Size:    ', field_dimensions['x_size'])
                print('Y Size:    ', field_dimensions['y_size'])
            if args.export_parsed_data_json:
                print('Exporting data...')
                export_parsed_data_json(video_prefix, frames, player_info,
                                        team_info)
                print('Export successful.')
            if args.export_parsed_data_csv:
                print('Exporting data...')
                export_parsed_data_csv(video_prefix, frames, player_info,
                                       team_info)
                print('Export successful.')
            if args.data_explorer:
                data_explorer_cli(data, actor_data, player_info, team_info,
                                  frames)
                exit()
            if args.render:
                print('Rendering video...')
                for render_type in args.render:
                    print('=====', 'Rendering', render_type, '=====')
                    render(render_type, assets_path, frames, player_info,
                           team_info, video_prefix)
                print('Render completed.')
            if args.render_all:
                print('Rendering video...')
                for render_type in available_assets:
                    print('=====', 'Rendering', render_type, '=====')
                    render(render_type, assets_path, frames, player_info,
                           team_info, video_prefix)
                print('Render completed.')


if __name__ == "__main__":
    main()
