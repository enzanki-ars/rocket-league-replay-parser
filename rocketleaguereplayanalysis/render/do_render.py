def render(filename, assets_path, frames, player_info, team_info,
           video_prefix):
    import json
    import os
    from rocketleaguereplayanalysis.render.ffmpeg_cmd import \
        create_ffmpeg_cmd_files_from_path, replace_in_array
    from rocketleaguereplayanalysis.util.transcode import \
        render_video

    with open(os.path.join(assets_path, filename + '.json')) as f:
        render_paths = json.load(f)

    is_player_render = False

    for render_cmd in render_paths:
        if 'modify' in render_cmd:
            if 'reinit' in render_cmd:
                create_ffmpeg_cmd_files_from_path(
                        frames=frames,
                        player_info=player_info,
                        team_info=team_info,
                        video_prefix=video_prefix,
                        path=render_cmd['variable_path'],
                        filter_type=render_cmd['filter'],
                        reinit=render_cmd['reinit'],
                        modify=render_cmd['modify'])
            else:
                create_ffmpeg_cmd_files_from_path(
                        frames=frames,
                        player_info=player_info,
                        team_info=team_info,
                        video_prefix=video_prefix,
                        path=render_cmd['variable_path'],
                        filter_type=render_cmd['filter'],
                        modify=render_cmd['modify'])
        else:
            if 'reinit' in render_cmd:
                create_ffmpeg_cmd_files_from_path(
                        frames=frames,
                        player_info=player_info,
                        team_info=team_info,
                        video_prefix=video_prefix,
                        path=render_cmd['variable_path'],
                        filter_type=render_cmd['filter'],
                        reinit=render_cmd['reinit'])
            else:
                create_ffmpeg_cmd_files_from_path(
                        frames=frames,
                        player_info=player_info,
                        team_info=team_info,
                        video_prefix=video_prefix,
                        path=render_cmd['variable_path'],
                        filter_type=render_cmd['filter'])

        if 'player_num' in render_cmd['variable_path']:
            is_player_render = True

    if is_player_render:
        for player in player_info.keys():
            extra_cmd_filter = ''

            for i, render_cmd in enumerate(render_paths, start=1):
                new_path = list(replace_in_array(render_cmd['variable_path'],
                                                 'player_num', player))
                new_name = '-'.join(str(x) for x in new_path)

                extra_cmd_filter += 'sendcmd=f=' + new_name + '.txt,' + \
                                    render_cmd['filter'] + '@' + new_name

                if render_cmd['filter'] == 'drawtext':
                    if 'font' not in render_cmd:
                        font = 'OpenSans.ttf'
                    else:
                        font = render_cmd['font']

                    extra_cmd_filter += '=fontfile=\\\'' + \
                                        os.path.join(assets_path,
                                                     font).replace(
                                                '\\', '\\\\') + '\\\''
                    if 'set_team_name' in render_cmd:
                        extra_cmd_filter += ':text=' + \
                                            team_info[
                                                player_info[player]['team']][
                                                'name']
                    if 'options' in render_cmd:
                        extra_cmd_filter += ':'
                elif render_cmd['filter'] == 'drawbox':
                    if 'set_team_color' in render_cmd:
                        extra_cmd_filter += '=color=' + \
                                            team_info[
                                                player_info[player]['team']][
                                                'color']
                    if 'options' in render_cmd:
                        extra_cmd_filter += ':'
                else:
                    if 'options' in render_cmd:
                        extra_cmd_filter += '='

                if 'options' in render_cmd:
                    for j, option_what in enumerate(
                            render_cmd['options'].keys(),
                            start=1):
                        extra_cmd_filter += option_what + '=' + \
                                            str(render_cmd['options'][
                                                    option_what])

                        if j != len(render_cmd['options'].keys()):
                            extra_cmd_filter += ':'

                if i != len(render_paths):
                    extra_cmd_filter += ','

            render_video(str(player) + '-' + filename, frames, video_prefix,
                         overlay=os.path.join(assets_path, filename),
                         extra_cmd=['-vf', extra_cmd_filter])
    else:
        extra_cmd_filter = ''

        for i, render_cmd in enumerate(render_paths, start=1):
            name = '-'.join(str(x) for x in render_cmd['variable_path'])

            extra_cmd_filter += 'sendcmd=f=' + name + '.txt,' + \
                                render_cmd['filter'] + '@' + name

            if render_cmd['filter'] == 'drawtext':
                if 'font' not in render_cmd:
                    font = 'OpenSans.ttf'
                else:
                    font = render_cmd['font']

                extra_cmd_filter += '=fontfile=\\\'' + \
                                    os.path.join(assets_path,
                                                 font).replace(
                                            '\\',
                                            '\\\\') + '\\\''
                if 'set_team_name' in render_cmd:
                    extra_cmd_filter += ':text=' + \
                                        team_info[render_cmd['set_team_name']][
                                            'name']
                if 'options' in render_cmd:
                    extra_cmd_filter += ':'
            elif render_cmd['filter'] == 'drawbox':
                if 'set_team_color' in render_cmd:
                    extra_cmd_filter += '=color=' + \
                                        team_info[render_cmd['set_team_color']][
                                            'color']
                if 'options' in render_cmd:
                    extra_cmd_filter += ':'
            else:
                if 'options' in render_cmd:
                    extra_cmd_filter += '='

            if 'options' in render_cmd:
                for j, option_what in enumerate(render_cmd['options'].keys(),
                                                start=1):
                    extra_cmd_filter += option_what + '=' + \
                                        str(render_cmd['options'][option_what])

                    if j != len(render_cmd['options'].keys()):
                        extra_cmd_filter += ':'

            if i != len(render_paths):
                extra_cmd_filter += ','

        render_video(filename, frames, video_prefix,
                     overlay=os.path.join(assets_path, filename),
                     extra_cmd=['-vf', extra_cmd_filter])
