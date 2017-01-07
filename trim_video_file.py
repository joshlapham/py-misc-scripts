#!/usr/bin/python

from os import path
from subprocess import Popen, PIPE
from argparse import ArgumentParser
from logger import Logger

logger = Logger()

FFMPEG_EXE = '/usr/local/bin/ffmpeg'

def _trim_video_file(video_filepath, output_filepath, start_time, end_time=None):
    CLI = None
    
    if end_time is None:
        CLI = [
            FFMPEG_EXE, '-i',
            '%s' % video_filepath,
            '-ss', '%s' % start_time,
            '-vcodec', 'copy', '-acodec', 'copy',
            '%s' % output_filepath
        ]
        
    else:
        CLI = [
            FFMPEG_EXE, '-i',
            '%s' % video_filepath,
            '-ss', '%s' % start_time,
            '-to', '%s' % end_time,
            '-vcodec', 'copy', '-acodec', 'copy',
            '%s' % output_filepath
        ]
        
    p = Popen(CLI, shell=False, stdout=PIPE, stderr=PIPE)
    return p
    
if __name__ == '__main__':
    """ Trims a video file with given start and end time values. """
    
    args = ArgumentParser()
    args.add_argument("--video-filepath", required=True)
    args.add_argument("--start-time", required=True)
    args.add_argument("--end-time", required=False)
    args = args.parse_args()

    ffmpeg_process = None

    try:
        logger.info("Trimming video file %s @ start time %s" % (args.video_filepath, args.start_time))
        base_filepath = path.splitext(args.video_filepath)[0]
        file_ext = path.splitext(args.video_filepath)[1]    
        output_filepath = '%s_edited%s' % (base_filepath, file_ext)
        logger.info("Saving to output file %s" % output_filepath)
        ffmpeg_process = _trim_video_file(args.video_filepath, output_filepath, args.start_time, args.end_time)
        stdout, stderr = ffmpeg_process.communicate()

    except StandardError as e:
        logger.error(e)
        ffmpeg_process.kill()
        exit()

    except KeyboardInterrupt:
        ffmpeg_process.kill()
        logger.info("User aborted script execution")
        exit()