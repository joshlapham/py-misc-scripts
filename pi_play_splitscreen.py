#!/usr/bin/python

import subprocess
import os
import glob
import random
import argparse
from logger import Logger
import omxplayer_split_cfg as cfg

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
            
def play_random_videos(parent_dir, all_videos, square=None, muted=True):
    global BASE_CLI
    global MUTED_CLI
    CLI_TO_USE = None
    
    already_played = []
    
    # TODO: should this bit of logic be called outside of this method?
    while len(already_played) != len(all_videos):
        random_video_filepath = random.choice(all_videos)
        
        found_unplayed = False
        
        while found_unplayed is False:
            if random_video_filepath not in already_played:
                found_unplayed = True
            else:
                random_video_filepath = random.choice(all_videos)
                found_unplayed = False
                
        CLI_TO_USE = list(BASE_CLI)
        
        # Use fullscreen if no `square` param was passed; otherwise 'squarify' playback
        if square is not None:
            square_cli = _cli_to_use_for_square(square)
            for item in square_cli:
                CLI_TO_USE.append(item)
                
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
    
    # TODO: add arg for `loop` -- play video files again once all have been played
    
    # TODO: these shouldn't be hardcoded, we should take a `parent_dir` arg or something, and allow for `path_to_glob`
    args.add_argument("--music-videos", action="store_true")
    args.add_argument("--random-cartoons", action="store_true")
    args.add_argument("--random-shows", action="store_true")
    args.add_argument("--nba-games", action="store_true")
    args.add_argument("--funny-videos", action="store_true")
    
    args.add_argument("--stream-url", required=False)
    
    args = args.parse_args()
    
    try:
        square_to_use = args.square
        
        if args.music_videos is True:
            # TODO: this should be arg, not hardcoded
            parent_dir = cfg.MUSIC_VIDEOS_PARENT_DIR
            
            # TODO: `path_to_glob` variables alternate between a prefix of '*/*' or '*' before the [] brackets; if we have array of shows/subdirs passed as arg then need to switch to use '*/*'
            path_to_glob = os.path.join(parent_dir, '*[.mp4, .flv, .mkv, .avi]')
            
            all_music_videos = glob.glob(path_to_glob)
            LOGGER.debug('Music videos: %i' % len(all_music_videos))
            
            # TODO: use `muted` arg here (add param to `play_random_videos` method)
            play_random_videos(parent_dir, all_music_videos, square=square_to_use)
            
        elif args.random_cartoons is True:
            # TODO: need to choose another random TV show; or pass args for option to do this
            # TODO: this logic needs rethinking
            # Right now we choose a random show only once at the start, then play random episodes from that show
            tv_shows_to_choose_from = cfg.CARTOONS_TO_CHOOSE_FROM
            random_tv_show_choice = random.choice(tv_shows_to_choose_from)
            
            parent_dir = ('%s/%s' % (cfg.TV_SHOWS_PARENT_DIR, random_tv_show_choice))
            path_to_glob = os.path.join(parent_dir, '*/*[.mp4, .flv, .mkv, .avi]')
            all_eps_of_random_tv_show = glob.glob(path_to_glob)
            LOGGER.debug('Cartoons: %i' % len(all_eps_of_random_tv_show))
            play_random_videos(parent_dir, all_eps_of_random_tv_show, square=square_to_use)
            
        elif args.random_shows is True:
            tv_shows_to_choose_from = cfg.TV_SHOWS_TO_CHOOSE_FROM
            random_tv_show_choice = random.choice(tv_shows_to_choose_from)
            parent_dir = ('%s/%s' % (cfg.TV_SHOWS_PARENT_DIR, random_tv_show_choice))    
            path_to_glob = os.path.join(parent_dir, '*/*[.mp4, .flv, .mkv, .avi]')
            all_eps_of_random_tv_show = glob.glob(path_to_glob)
            LOGGER.debug('TV Shows: %i' % len(all_eps_of_random_tv_show))
            play_random_videos(parent_dir, all_eps_of_random_tv_show, square=square_to_use)
            
        elif args.nba_games is True:
            parent_dir = cfg.NBA_PARENT_DIR  
            path_to_glob = os.path.join(parent_dir, '*[.mp4, .flv, .mkv, .avi]')
            nba_games = glob.glob(path_to_glob)
            LOGGER.debug('NBA games: %i' % len(nba_games))
            play_random_videos(parent_dir, nba_games, square=square_to_use)
            
        elif args.funny_videos is True:
            parent_dir = cfg.FUNNY_VIDEOS_PARENT_DIR  
            path_to_glob = os.path.join(parent_dir, '*[.mp4, .flv, .mkv, .avi]')
            funny_videos = glob.glob(path_to_glob)
            LOGGER.debug('Funny videos: %i' % len(funny_videos))
            play_random_videos(parent_dir, funny_videos, square=square_to_use)
            
        elif args.stream_url is not None:
            LOGGER.debug('Streaming from: %s' % args.stream_url)
            play_stream(args.stream_url, square_to_use)
            
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
        
else:
    pass