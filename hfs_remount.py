#!/bin/python

from os import path
from subprocess import check_output
from argparse import ArgumentParser

def unount_if_mounted(drive_path):
    """ Unmount given drive path, if mounted. """
    
    filesystem_unmount_cli = [
        'sudo',
        'umount',
        drive_path
    ]
    
    if path.ismount(drive_path) is True:
        print "Unmounting filesystem .."
        
        try:
            check_output(filesystem_unmount_cli)

        except:
            raise Exception("Failed to unmount filesystem")
            
def mount_if_unmounted(drive_path):
    """ Mount given drive path, if not mounted. """
    
    filesystem_mount_cli = [
        'sudo',
        'mount', '-a'
    ]
    
    if path.ismount(drive_path) == False:
        print "Mounting filesystem .."
        
        try:
            check_output(filesystem_mount_cli)

        except:
            raise Exception("Failed to mount filesystem")

# Filesystem check
def do_filesystem_check(device_path):
    check_filesystem_cli = [
        'sudo',
        'fsck.hfsplus', '-fy',
        device_path
    ]
    
    print "Checking filesystem .."
    
    try:
        check_output(check_filesystem_cli)

    except:
        raise Exception("Failed to perform filesystem check")

# Main
if __name__ == "__main__":
    args = ArgumentParser(description='Unmount a given HFS drive, do filesystem check and re-mount.')
    args.add_argument('--drive-path', help='Filesystem path for HFS drive', required=True)
    args.add_argument('--device-path', help='Device path for HFS drive, e.g. "/dev/sda2"', required=True)
    args = args.parse_args()

    try:
        unount_if_mounted(args.drive_path)
        do_filesystem_check(args.device_path)
        mount_if_unmounted(args.drive_path)
        
        print "\nFilesystem has been checked and re-mounted."

    except Exception as e:
        print "\n## Error : " % e
