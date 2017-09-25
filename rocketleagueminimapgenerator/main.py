import argparse
import os

from rocketleagueminimapgenerator.actor_data import parse_actor_data
from rocketleagueminimapgenerator.data import load_data, set_data_end
from rocketleagueminimapgenerator.frames import load_frames
from rocketleagueminimapgenerator.object_numbers import parse_ball_obj_nums, \
    parse_car_obj_nums, parse_player_info
from rocketleagueminimapgenerator.render import render_field, render_video

with open('field-template.svg', 'r') as svg_file:
    field_template = svg_file.read()

car_template = '<circle class="team{team_id} stroke-black" ' \
               'cx="{car_pos_x}" cy="{car_pos_y}" r="{car_size}"/>' \
               '<polygon class="team{team_id} stroke-black" ' \
               'points="' \
               '{car_triangle_pt1_x},{car_triangle_pt1_y} ' \
               '{car_triangle_pt2_x},{car_triangle_pt2_y} ' \
               '{car_triangle_pt3_x},{car_triangle_pt3_y} " ' \
               'transform="rotate({car_angle} {car_pos_x} {car_pos_y})' \
               'translate(0 -{arrow_move})"/>'
frame_num_format = '{0:04d}'


def main():
    parser = argparse.ArgumentParser(prog='rocketleagueminimapgenerator')

    # Required args
    parser.add_argument('game_json', help='The name of the game json.')

    # Optional args
    parser.add_argument('--data_end', help='Number of frames to render.',
                        type=int)

    args = parser.parse_args()

    out_prefix = args.game_json

    load_data(out_prefix)

    if args.data_end:
        set_data_end(args.data_end)

    parse_actor_data()

    parse_ball_obj_nums()
    parse_car_obj_nums()
    parse_player_info()

    load_frames()

    video_prefix = os.path.join('renders', out_prefix.split('.')[0])

    render_field(video_prefix)

    render_video(video_prefix)


if __name__ == "__main__":
    main()
