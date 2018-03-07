def render_video(render_type, frames, video_prefix,
                 out_frame_rate=30, overlay=None, extra_cmd=None):
    import os
    import subprocess

    from rocketleaguereplayanalysis.util.sync import get_sync_time_type

    cmd = ['ffmpeg',
           '-loop', '1',
           '-i', os.path.join('assets', overlay + '.png'),
           '-t', str(frames[-1]['time'][get_sync_time_type()])]

    cmd += extra_cmd

    cmd += ['-r', str(out_frame_rate),
            '-crf', '18',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            render_type + '.mp4', '-y']

    print('FFmpeg Command:', cmd)

    p = subprocess.Popen(cmd, cwd=video_prefix, stderr=subprocess.STDOUT)

    p.communicate()
