import os
import shutil
import subprocess
from pathlib import Path

import cairosvg
from tqdm import tqdm


def render_field(out_prefix):
    from rocketleagueminimapgenerator.frames import get_frames
    from rocketleagueminimapgenerator.data import get_data_end
    from rocketleagueminimapgenerator.config import get_config

    frames = get_frames()

    ball_loc = {'x': [], 'y': []}

    for frame in frames:
        ball_loc['x'].append(frame['ball']['loc']['x'])
        ball_loc['y'].append(frame['ball']['loc']['y'])

    max_x = max(ball_loc['x'])
    min_x = min(ball_loc['x'])
    x_w = max_x - min_x

    # Make divisible by 2
    x_size = ((x_w - (x_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    max_y = max(ball_loc['y'])
    min_y = min(ball_loc['y'])
    y_w = max_y - min_y

    # Make divisible by 2
    y_size = ((y_w - (y_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    print('X:', x_size, 'Y:', y_size, 'Ball:', get_config('ball_size'))

    if os.path.exists(out_prefix):
        shutil.rmtree(out_prefix)

    if not os.path.exists(out_prefix):
        path = Path(out_prefix)
        path.mkdir(parents=True)

    for i in tqdm(range(0, get_data_end()), desc='Video Frame Out',
                  ascii=True):
        render_frame(ball_loc=ball_loc, frames=frames, frame_num=i,
                     min_x=min_x, min_y=min_y, out_prefix=out_prefix,
                     x_size=x_size, y_size=y_size)


def render_frame(ball_loc, frames, frame_num,
                 min_x, min_y, x_size, y_size, out_prefix):
    import math
    from rocketleagueminimapgenerator.main import frame_num_format, \
        car_template, field_template
    from rocketleagueminimapgenerator.object_numbers import \
        get_player_info
    from rocketleagueminimapgenerator.config import \
        get_config

    with open(os.path.join(out_prefix,
                           frame_num_format.format(frame_num) + '.png'),
              'wb') as file_out:
        car_placement = ''

        car_size = get_config('car_size')

        r = car_size / 2

        tri_pt_x_const = r / 2 * math.sqrt(3)
        tri_pt_y_const = r / math.sqrt(3)

        for car_id in frames[frame_num]['cars'].keys():
            if frames[frame_num]['cars'][car_id]['loc']['x'] and \
                    frames[frame_num]['cars'][car_id]['loc']['y']:
                car_pos_x = (frames[frame_num]['cars'][car_id]['loc']['x']
                             - min_x) / get_config('size_modifier')
                car_pos_y = (frames[frame_num]['cars'][car_id]['loc']['y']
                             - min_y) / get_config('size_modifier')
                car_show_size = car_size
            else:
                car_pos_x = -10000
                car_pos_y = -10000
                car_show_size = 0

            car_placement += car_template.format(
                    team_id=get_player_info()[car_id]['team'],
                    car_pos_x=car_pos_x,
                    car_pos_y=car_pos_y,

                    car_triangle_pt1_x=car_pos_x,
                    car_triangle_pt1_y=car_pos_y - r,

                    car_triangle_pt2_x=car_pos_x - tri_pt_x_const,
                    car_triangle_pt2_y=car_pos_y + tri_pt_y_const,

                    car_triangle_pt3_x=car_pos_x + tri_pt_x_const,
                    car_triangle_pt3_y=car_pos_y + tri_pt_y_const,

                    car_angle=(frames[frame_num]['cars'][car_id]['rot']['y'] +
                               90),

                    car_size=car_show_size,
                    arrow_move=car_show_size * 1.5
            )

        cairosvg.svg2png(bytestring=bytes(
                field_template.format(x_size=x_size,
                                      y_size=y_size,
                                      center_pos_x=x_size / 2,
                                      center_pos_y=y_size / 2,
                                      center_size=get_config('center_size'),
                                      ball_pos_x=(ball_loc['x'][frame_num] -
                                                  min_x) / get_config(
                                              'size_modifier'),
                                      ball_pos_y=(ball_loc['y'][frame_num] -
                                                  min_y) / get_config(
                                              'size_modifier'),
                                      ball_size=get_config('ball_size'),
                                      car_placement=car_placement
                                      ), 'UTF-8'), write_to=file_out)


def render_video(out_prefix, out_frame_rate=30):
    from rocketleagueminimapgenerator.frames import get_frames
    from rocketleagueminimapgenerator.main import frame_num_format
    from rocketleagueminimapgenerator.data import get_data_end

    Path(out_prefix + '-frames.txt').touch()

    with open(out_prefix + '-frames.txt', 'w') as f:
        out_str = ''
        for i, frame in enumerate(get_frames()[:get_data_end()]):
            out_str += 'file \'' + os.path.join(out_prefix,
                                                frame_num_format.format(
                                                        i) +
                                                '.png') + '\'\n'
            out_str += 'duration ' + str(frame['delta']) + '\n'
        # Ensure display of final frame
        out_str += 'file \'' + os.path.join(out_prefix,
                                            frame_num_format.format(
                                                    get_data_end()) +
                                            '.png') + '\'\n'
        f.write(out_str)

    p = subprocess.Popen(['ffmpeg',
                          '-safe', '0',
                          '-f', 'concat',
                          '-i', out_prefix + '-frames.txt',
                          '-r', str(out_frame_rate),
                          '-vf', 'format=yuv420p',
                          '-crf', '18',
                          os.path.join(out_prefix + '.mp4'),
                          '-y'],
                         stderr=subprocess.STDOUT)

    stdout, stderr = p.communicate()
