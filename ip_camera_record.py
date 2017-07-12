#!/bin/python

import subprocess
import time
import sys
import logger
import argparse

FFMPEG_EXE = '/usr/local/bin/ffmpeg'

# TODO: use DI for logger
LOGGER = logger.Logger()

def _do_timelapse(file, output_file):
    # TODO: form CLI string to turn a video file into a timelapse video
    pass

def _do_archive():
    # TODO: parse files that are older than a certain amount of days
    # TODO: convert files to lower bitrate and quality
    # TODO: concatenate files into one video file
    pass

def _do_join(date):
    # TODO: parse files for given `date`
    # TODO: form CLI string for list of files
    pass

def _do_record(stream_url, output_path):
    filename = "{}.mp4".format(time.strftime("%Y%m%d-%H%M%S"))

    LOGGER.info('Recording to file {}'.format(filename))

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

        LOGGER.info('Finished recording to file {}'.format(filename))

    except subprocess.CalledProcessError as e:
        LOGGER.info(e)

    except Exception as e:
        # TODO: might just need to call `raise` without the `e`?
        raise Exception(e)

if __name__ == "__main__":
    """ Records RTSP stream from an IP camera using ffmpeg. """

    parser = argparse.ArgumentParser()
    parser.add_argument('--stream-url', help='RTSP stream URL', type=str, required=True)
    parser.add_argument('--output-path', help='Path for recorded output', type=str, required=True)
    args = parser.parse_args()

    # TODO: remove
    # rtsp://192.168.1.38:554/onvif1
    # /Volumes/Media/ip_camera

    try:
        _do_record()

    except KeyboardInterrupt:
        sys.exit('User aborted script execution')

    except Exception as e:
        LOGGER.info('Exception: {}'.format(e))
