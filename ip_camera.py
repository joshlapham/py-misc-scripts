#!/bin/python

import subprocess
import time
import sys
import logger
import argparse

FFMPEG_EXE = '/usr/local/bin/ffmpeg'

def _do_frame_snapshot(stream_url, output_path, logger=None):
    # TODO: take snapshot of `stream_url` using `ffmpeg`
    # TODO: output snapshot to `output_path`
    # TODO: handle filename > use dimensions of image in name
    pass
    
def _do_timelapse(file, output_file):
    # TODO: turn a video file into a timelapse video
    pass

def _do_archive():
    # TODO: join all videos for given `date` / older than a certain amount of days
    # TODO: convert files to lower bitrate and quality
    # TODO: concatenate files into one video file
    pass

def _do_record(stream_url, output_path, logger):
    filename = "{}.mp4".format(time.strftime("%Y%m%d-%H%M%S"))

    logger.info('Recording to file {}'.format(filename))

    # TODO: use arg for `900` value in `CLI`

    CLI = [
        '{}'.format(FFMPEG_EXE),
        '-i', '{}'.format(stream_url),
        '-r', '30',
        '-vcodec', 'copy',
        '-an',
        '-t', '900',
        '{}/{}'.format(output_path, filename)
    ]

    try:
        p = subprocess.Popen(CLI, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        logger.info('Finished recording to file {}'.format(filename))

    except subprocess.CalledProcessError as e:
        logger.info(e)

    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    """ Record/take pictures from an IP camera RTSP stream using `ffmpeg`. """

    # TODO: handle argument for snapshots -- call `_do_frame_snapshot`
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--stream-url', help='RTSP stream URL', type=str, required=True)
    parser.add_argument('--output-path', help='Path for recorded output', type=str, required=True)
    args = parser.parse_args()

    # TODO: remove
    # rtsp://192.168.1.38:554/onvif1
    # /Volumes/Media/ip_camera

    logger = logger.Logger()

    try:
        _do_record(args.stream_url, args.output_path, logger)

    except KeyboardInterrupt:
        sys.exit('User aborted script execution')

    except Exception as e:
        logger.info('Exception: {}'.format(e))
