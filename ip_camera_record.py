#!/bin/python

import subprocess
import time
import sys
from logger import Logger

FFMPEG_EXE = '/usr/local/bin/ffmpeg'

LOGGER = Logger()

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

def _do_record():
    output_filepath = time.strftime("%Y%m%d-%H%M%S")

    LOGGER.info('Recording to file %s.mp4' % output_filepath)

    # TODO: take params to this method; don't hardcode values
    CLI = [
        '%s' % FFMPEG_EXE,
        '-i', 'rtsp://192.168.1.38:554/onvif1',
        '-r', '30',
        '-vcodec', 'copy',
        '-an',
        '-t', '900',
        '/Volumes/Media/ip_camera/%s.mp4' % output_filepath
    ]

    try:
        p = subprocess.Popen(CLI, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        LOGGER.info('Finished recording to file %s.mp4' % output_filepath)

    except subprocess.CalledProcessError as e:
        LOGGER.info(e)

    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    # TODO: accept command-line args
    # TODO: write doc header for this script

    try:
        _do_record()

    except KeyboardInterrupt:
        LOGGER.info('User aborted script execution')
        sys.exit(1)

    except Exception as e:
        LOGGER.info('Exception: %s' % e)