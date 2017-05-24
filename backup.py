#!/usr/bin/python

from os import path
from threading import Thread
from argparse import ArgumentParser
from subprocess import CalledProcessError
from prowl_notify import post_to_prowl
from logger import Logger
from command_helpers import do_command
from kodi_library_update import do_video_library_scan, do_video_library_clean
import backup_cfg as cfg

logger = Logger()

def _notify(event_text, description_text):
    thread = Thread(target=post_to_prowl, args=[cfg.PROWL_TITLE, event_text, description_text])
    thread.start()
    
def _kodi_library_update(clean=False):
    update_thread = Thread(target=do_video_library_scan)
    update_thread.start()
    
    if clean is True:
        clean_thread = Thread(target=do_video_library_clean)
        clean_thread.start()
        
def _backup(target, destination, preserve_timestamps=True):
    ignore_timestamps_options = '-rltDvPhz'
    normal_options = '-avPhz'
    options_to_use = normal_options
    
    if preserve_timestamps is False:
        options_to_use = ignore_timestamps_options
        
    cli = [
        "rsync",
        "%s" % options_to_use,
        "--exclude", ".DocumentRevisions-V100", "--exclude", ".Trashes",
        "--delete-before",
        "%s" % target,
        "%s" % destination,
    ]
    
    do_command(cli, own_process=False)
    
def do_backup(args):
    # Media HD
    if args.media is True and path.exists(cfg.MEDIA_HD_TARGET) is True and path.exists(cfg.MEDIA_HD_DESTINATION) is True:
        # Movies
        logger.info("Backing up Movies ..")
        
        if args.notify:
            _notify("Backup Started", "Backup from %s to %s started" % (cfg.MEDIA_HD_MOVIES_TARGET, cfg.MEDIA_HD_MOVIES_DESTINATION))
            
        try:
            _backup(cfg.MEDIA_HD_MOVIES_TARGET, cfg.MEDIA_HD_MOVIES_DESTINATION, preserve_timestamps=False)
            logger.info("Backup successful")
            
            if args.notify:
                _notify("Backup Complete", "Backup from %s to %s completed" % (cfg.MEDIA_HD_MOVIES_TARGET, cfg.MEDIA_HD_MOVIES_DESTINATION))
                
            if args.update_kodi:
                _kodi_library_update()
                logger.info("Sent update command to Kodi Media Library")
                
        except Exception as e:
            logger.error(e)
            
            if args.notify:
                _notify("Backup Error", "Backup from %s to %s error!\n%s" % (cfg.MEDIA_HD_MOVIES_TARGET, cfg.MEDIA_HD_MOVIES_DESTINATION), e)
                
        # TV Shows
        logger.info("Backing up TV Shows ..")
        
        if args.notify:
            _notify("Backup Started", "Backup from %s to %s started" % (cfg.MEDIA_HD_TV_TARGET, cfg.MEDIA_HD_TV_DESTINATION))
            
        try:
            _backup(cfg.MEDIA_HD_TV_TARGET, cfg.MEDIA_HD_TV_DESTINATION, preserve_timestamps=False)
            logger.info("Backup successful")
            
            if args.notify:
                _notify("Backup Complete", "Backup from %s to %s completed" % (cfg.MEDIA_HD_TV_TARGET, cfg.MEDIA_HD_TV_DESTINATION))
                
            if args.update_kodi:
                _kodi_library_update(clean=args.clean)
                logger.info("Sent update command to Kodi Media Library")
                
        except Exception as e:
            logger.error(e)
            
            if args.notify:
                _notify("Backup Error", "Backup from %s to %s error!\n%s" % (cfg.MEDIA_HD_TV_TARGET, cfg.MEDIA_HD_TV_DESTINATION), e)
                
    # Files HD
    if args.files is True and path.exists(cfg.FILES_HD_DESTINATION) is True and path.exists(cfg.FILES_HD_TARGET) is True:
        logger.info("Backing up Files HD ..")
        
        if args.notify:
            _notify("Backup Started", "Backup from %s to %s started" % (cfg.FILES_HD_TARGET, cfg.FILES_HD_DESTINATION))
            
        try:
            _backup(cfg.FILES_HD_TARGET, cfg.FILES_HD_DESTINATION)
            logger.info("Backup successful")
            
            if args.notify:
                _notify("Backup Complete", "Backup from %s to %s completed" % (cfg.FILES_HD_TARGET, cfg.FILES_HD_DESTINATION))
                
        except StandardError as e:
            if args.notify:
                _notify("Backup Error", "Backup from %s to %s error!\n%s" % (cfg.FILES_HD_TARGET, cfg.FILES_HD_DESTINATION), e)
                
            raise StandardError(e)
            
if __name__ == '__main__':
    args = ArgumentParser(description="Backup stuff")
    group = args.add_mutually_exclusive_group(required=True)
    group.add_argument("--files", help="Do backup of Files HD", action="store_true")
    group.add_argument("--media", help="Do backup of Media HD", action="store_true")
    args.add_argument("--notify", help="Send notifications", action="store_true")
    args.add_argument("--update-kodi", help="Update Kodi Media Library", action="store_true")
    args.add_argument("--clean", help="Make API call to clean the video library", action="store_true")
    args = args.parse_args()
    
    if args.notify:
        logger.info("Notifcations enabled")
        
    try:
        do_backup(args)
        
    except KeyboardInterrupt:
        logger.info("User aborted script execution")
        
    except StandardError as e:
        logger.error("Error calling command in own process: %s" % e)
        
    except CalledProcessError as e:
        logger.error("Error calling command: %s" % e)
        
    except Exception as e:
        logger.error(e)
        