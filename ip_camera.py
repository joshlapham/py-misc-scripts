#!/bin/python3

import subprocess
import time
import sys
import logger
import argparse

FFMPEG_EXE = '/usr/local/bin/ffmpeg'

def _do_frame_snapshot(stream_url, output_path, logger=None):
    # TODO: handle filename > use dimensions of image in name
    
    filename = "{}.jpg".format(time.strftime("%Y%m%d-%H%M%S"))
    
    CLI = [
        '{}'.format(FFMPEG_EXE),
        '-y',
        '-i', '{}'.format(stream_url),
        '-vframes', '1',
        '{}/{}'.format(output_path, filename)
    ]
    
    try:
        p = subprocess.Popen(CLI, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        logger.info('Finished taking snapshot to file {}'.format(filename))

    except subprocess.CalledProcessError as e:
        logger.info(e)

    except Exception as e:
        raise Exception(e)
        
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

    # TODO: if `stream_url` is not a valid stream URL, then there will be no output file -- need to do error handling
    
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--stream-url', help='RTSP stream URL', type=str, required=True)
    parser.add_argument('--output-path', help='Path for recorded output', type=str, required=True)
    parser.add_argument('--snapshot-only', help='Take a snapshot of the RTSP stream URL and save to JPEG file', action='store_true', required=False, default=False)
    args = parser.parse_args()

    logger = logger.Logger()

    try:
        if args.snapshot_only is True:
            _do_frame_snapshot(args.stream_url, args.output_path, logger)
        else:
            _do_record(args.stream_url, args.output_path, logger)
            
    except KeyboardInterrupt:
        sys.exit('User aborted script execution')

    except Exception as e:
        logger.info('Exception: {}'.format(e))
