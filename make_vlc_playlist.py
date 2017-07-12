#!/usr/bin/python

from glob import glob
from os import path
from subprocess import Popen, PIPE
from argparse import ArgumentParser
from logger import Logger

VLC_EXE = '/Applications/VLC.app/Contents/MacOS/VLC'

logger = Logger()

def _generate_playlist(results, playlist_path):
    results_ordered = list(enumerate(results, start=1))
    
    with open(playlist_path, 'w') as playlist_file:
        playlist_file.write("[playlist]\n")
        playlist_file.write("NumberOfEntries=%s\n" % str(len(results)))
        
        for video in results_ordered:
            number = video[0]
            filepath = video[1]
            playlist_file.write("File%s=%s\n" % (str(number), filepath))
            playlist_file.write("Title%s=%s\n" % (str(number), filepath))
            
        playlist_file.close()

def _open_in_vlc(playlist_path):
    cli = [
        '%s' % VLC_EXE,
        '%s' % playlist_path
    ]
    
    p = Popen(cli, shell=False, stdout=PIPE, stderr=PIPE)
    return p
            
def _search_video_files(parent_dir):
    # TODO: review this line
    # For subdirectories
    # path_to_glob = path.join(parent_dir, '*/*[.mp4, .flv, .mkv]')
    # For parent only
    path_to_glob = path.join(parent_dir, '*[.mp4, .flv, .mkv]')
    results = glob(path_to_glob)
    return results
    
if __name__ == '__main__':
    """ Creates a playlist of all video files from a given directory (including all subdirectories) and opens in VLC for playback. """
    
    args = ArgumentParser()
    args.add_argument("--parent-dir", required=True)
    args.add_argument("--playlist-path", required=True)
    args = args.parse_args()
    
    vlc_process = None
    
    try:
        results = _search_video_files(args.parent_dir)
        logger.info("Found %s results" % str(len(results)))
        _generate_playlist(results, args.playlist_path)
        logger.info("Generated playlist")
        logger.info("Opening playlist in VLC")
        vlc_process = _open_in_vlc(args.playlist_path)
        stdout, stderr = vlc_process.communicate()
        
    except StandardError as e:
        logger.error(e)
        vlc_process.kill()
        exit()
        
    except KeyboardInterrupt:
        vlc_process.kill()
        logger.info("User aborted script execution")
        exit()
        