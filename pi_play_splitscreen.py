#!/usr/bin/python

import subprocess
import os
import glob
import random
import argparse
from logger import Logger

LOGGER = Logger()
OMXPLAYER_EXE = 'omxplayer'
PROCESSES = []

BASE_CLI = ['%s' % OMXPLAYER_EXE]
MUTED_CLI = ['-n', '-1']
SQUARE_1_CLI = ['--win', '0 0 960 540']
SQUARE_2_CLI = ['--win', '960 0 1920 540']
SQUARE_3_CLI = ['--win', '0 540 960 1080']
SQUARE_4_CLI = ['--win', '960 540 1920 1080 1080']

def play_stream(stream_url=None, square=None):
    # TODO: finish implementing method
    
    # TODO: this will crash if `square` is None
    CLI_TO_USE = _cli_to_use_for_square(square)
    
    if stream_url is not None:
        CLI_TO_USE.append(stream_url)
        
        LOGGER.debug('CLI: %s' % CLI_TO_USE)
        
        try:
            LOGGER.info('Streaming URL: %s' % stream_url)
            p = subprocess.Popen(CLI_TO_USE, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            PROCESSES.append(p)
            p.wait()
                
        except subprocess.CalledProcessError as e:
            LOGGER.info('Omxplayer error when playing stream URL %s: %s' % (stream_url, e))
            
        except Exception as e:
            raise Exception(e)
            
def play_random_videos(video_files, square=None, muted=True):
    global BASE_CLI
    global MUTED_CLI
    CLI_TO_USE = None
    
    already_played = []
    
    # TODO: should this bit of logic be called outside of this method?
    while len(already_played) != len(video_files):
        random_video_filepath = random.choice(video_files)
        
        found_unplayed = False
        
        while found_unplayed is False:
            if random_video_filepath not in already_played:
                found_unplayed = True
            else:
                random_video_filepath = random.choice(video_files)
                found_unplayed = False
                
        CLI_TO_USE = list(BASE_CLI)
        
        # Use fullscreen if no `square` param was passed; otherwise 'squarify' playback
        if square is not None:
            LOGGER.debug('Square: %s' % square)
            
            square_cli = _cli_to_use_for_square(square)
            
            for item in square_cli:
                CLI_TO_USE.append(item)
                
        else:
            LOGGER.debug('Using fullscreen')
            
        # Mute/unmute audio
        if muted is not False:
            for item in MUTED_CLI:
                CLI_TO_USE.append(item)
                
        CLI_TO_USE.append(random_video_filepath)
        
        try:
            LOGGER.info('Now playing: %s' % random_video_filepath)
            
            already_played.append(random_video_filepath)
                
            p = subprocess.Popen(CLI_TO_USE, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            PROCESSES.append(p)
            p.wait()
            
            # Reset CLI
            CLI_TO_USE = None
                                                        
        except subprocess.CalledProcessError as e:
            LOGGER.info('Omxplayer error when playing file %s: %s' % (random_video_filepath, e))
            already_played.append(random_video_filepath)
            
        except Exception as e:
            raise Exception(e)
            
    else:
        LOGGER.info('Have played all videos!')
        
def _cli_to_use_for_square(square=None):
    if square is str(1):
        return SQUARE_1_CLI
    elif square is str(2):
        return SQUARE_2_CLI
    elif square is str(3):
        return SQUARE_3_CLI
    elif square is str(4):
        return SQUARE_4_CLI
    else:
        return None
        
def _kill_running_processes():
    running_count = 0

    for p in PROCESSES:
        if p.poll() is None:
            running_count = running_count + 1
            p.terminate()
            
    LOGGER.info('Terminated %i running processes' % running_count)
    
if __name__ == '__main__':
    args = argparse.ArgumentParser(description="Play videos in a square layout using `omxplayer` on a Raspberry Pi")
    args.add_argument("--square", help="Which square to play video in (1-4)", required=False)
    args.add_argument("--stream-url", required=False)    
    args.add_argument("--shows", required=False)
    args.add_argument("--parent-dir", required=False)
    
    # TODO: add arg for `loop` -- play video files again once all have been played
    
    args = args.parse_args()
    
    # If `shows` arg was specified, then glob needs to allow for subdirectories
    glob_to_use = None
    if args.shows is not None:
        glob_to_use = '*/*[.mp4, .flv, .mkv, .avi]'
    else:
        glob_to_use = '*[.mp4, .flv, .mkv, .avi]'
            
    try:
        if args.shows is not None:
            # TODO: this logic needs rethinking. Right now we choose a random show only once at the start, then play random episodes from that show. We need to loop and keep choosing a random show; but also allow for episodes to not be played again. Maybe this logic could be in `play_random_videos` method? So we'd loop over random shows, then within that method we'd choose a random episode. Alternatively, we load ALL episodes from `tv_shows_to_choose_from`, then randomize.
            
            tv_shows_to_choose_from = args.shows.split(', ')
            random_tv_show_choice = random.choice(tv_shows_to_choose_from)
            LOGGER.debug(random_tv_show_choice)
            
            parent_dir = ('%s/%s' % (args.parent_dir, random_tv_show_choice))
            path_to_glob = os.path.join(parent_dir, glob_to_use)
            videos_to_play = glob.glob(path_to_glob)
            LOGGER.debug('Videos: %i' % len(videos_to_play))
            play_random_videos(videos_to_play, square=args.square)
            
        elif args.stream_url is not None:
            LOGGER.debug('Streaming from: %s' % args.stream_url)
            play_stream(args.stream_url, args.square)
            
        else:
            parent_dir = args.parent_dir
            path_to_glob = os.path.join(parent_dir, glob_to_use)
            videos_to_play = glob.glob(path_to_glob)
            LOGGER.debug('Videos: %i' % len(videos_to_play))
            play_random_videos(videos_to_play, square=args.square)
            
        # Wait for all processes
        for p in PROCESSES:
            LOGGER.debug(p.pid)
            
        exit_codes = [p.wait() for p in PROCESSES]
        
        LOGGER.debug(exit_codes)
    
    except KeyboardInterrupt:
        LOGGER.info('User aborted script execution')
        _kill_running_processes()
        
    except Exception as e:
        LOGGER.debug('Exception: %s' % e)
        _kill_running_processes()
        