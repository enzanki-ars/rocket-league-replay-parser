import os
import shutil
import subprocess
from pathlib import Path

import cairosvg
from tqdm import tqdm


def find_scale():
    from rocketleagueminimapgenerator.frames import get_frames
    from rocketleagueminimapgenerator.config import get_config

    frames = get_frames()

    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0

    for frame in frames:
        ball_x = frame['ball']['loc']['x']
        ball_y = frame['ball']['loc']['y']

        if ball_x > max_x:
            max_x = ball_x
        elif ball_x < min_x:
            min_x = ball_x

        if ball_y > max_y:
            max_y = ball_y
        elif ball_y < min_y:
            min_y = ball_y

        for car_id in frame['cars'].keys():
            car_x = frame['cars'][car_id]['loc']['x']
            car_y = frame['cars'][car_id]['loc']['y']

            if car_x > max_x:
                max_x = car_x
            elif car_x < min_x:
                min_x = car_x

            if car_y > max_y:
                max_y = car_y
            elif car_y < min_y:
                min_y = car_y

    x_w = max_x - min_x

    y_w = max_y - min_y

    scale = x_w / get_config('image_width')

    print('X W:', x_w, 'Y W:', y_w, 'Scale:', scale)

    return x_w, y_w, scale


def render_field(out_prefix):
    from rocketleagueminimapgenerator.frames import get_frames
    from rocketleagueminimapgenerator.data import get_data_start, get_data_end

    frames = get_frames()

    x_w, y_w, scale = find_scale()

    if os.path.exists(out_prefix):
        shutil.rmtree(out_prefix)

    if not os.path.exists(out_prefix):
        path = Path(out_prefix)
        path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Video Frame Out', ascii=True):
        render_frame(frames=frames, frame_num=i, out_prefix=out_prefix,
                     x_size=x_w, y_size=y_w, scale=scale)


def render_frame(frames, frame_num, out_prefix, x_size, y_size, scale):
    import math
    from rocketleagueminimapgenerator.main import frame_num_format, \
        car_template, field_template
    from rocketleagueminimapgenerator.object_numbers import get_player_info
    from rocketleagueminimapgenerator.config import get_config

    with open(os.path.join(out_prefix,
                           frame_num_format.format(frame_num) + '.png'),
              'wb') as file_out:
        car_placement = ''

        car_size = get_config('car_size')

        r = car_size / 2

        tri_pt_x_const = r / 2 * math.sqrt(3)
        tri_pt_y_const = r / math.sqrt(3)

        y_mod = get_config('y_mod')

        for car_id in frames[frame_num]['cars'].keys():
            car_x = ((frames[frame_num]['cars'][car_id]['loc']['x'] + (
                x_size / 2)) / scale)
            car_y = ((frames[frame_num]['cars'][car_id]['loc']['y'] + (
                y_size / 2)) / scale) + y_mod

            # print('Car ID:', car_id, 'Car X:', car_x, 'Car Y:', car_y)

            car_placement += car_template.format(
                    team_id=get_player_info()[car_id]['team'],
                    car_pos_x=car_x,
                    car_pos_y=car_y,

                    car_triangle_pt1_x=car_x,
                    car_triangle_pt1_y=car_y - r,

                    car_triangle_pt2_x=car_x - tri_pt_x_const,
                    car_triangle_pt2_y=car_y + tri_pt_y_const,

                    car_triangle_pt3_x=car_x + tri_pt_x_const,
                    car_triangle_pt3_y=car_y + tri_pt_y_const,

                    car_angle=(frames[frame_num]['cars'][car_id]['rot']['y'] +
                               90),

                    car_size=car_size,
                    arrow_move=car_size * 1.5
            )

        ball_x = (
            (frames[frame_num]['ball']['loc']['x'] + (x_size / 2)) / scale)
        ball_y = ((frames[frame_num]['ball']['loc']['y'] + (
            y_size / 2)) / scale) + y_mod

        # print('Ball:', 'Ball X:', ball_x, 'Ball Y:', ball_y)

        cairosvg.svg2png(bytestring=bytes(
                field_template.format(ball_pos_x=ball_x,
                                      ball_pos_y=ball_y,

                                      ball_size=get_config('ball_size'),

                                      x_size=x_size,
                                      y_size=y_size,

                                      car_placement=car_placement
                                      ), 'UTF-8'), write_to=file_out)


def render_video(out_prefix, out_frame_rate=30):
    from rocketleagueminimapgenerator.frames import get_frames
    from rocketleagueminimapgenerator.main import frame_num_format
    from rocketleagueminimapgenerator.data import get_data_start, get_data_end

    Path(out_prefix + '-frames.txt').touch()

    with open(out_prefix + '-frames.txt', 'w') as f:
        out_str = ''
        for i, frame in enumerate(
                get_frames()[get_data_start():get_data_end()]):
            out_str += 'file \'' + os.path.join(out_prefix,
                                                frame_num_format.format(
                                                        i) + '.png') + '\'\n'
            out_str += 'duration ' + str(frame['delta']) + '\n'
        # Ensure display of final frame
        out_str += 'file \'' + os.path.join(out_prefix,
                                            frame_num_format.format(
                                                    get_data_end()) + '.png') + \
                   '\'\n'
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
