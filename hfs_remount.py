#!/bin/python

from subprocess import check_output
from argparse import ArgumentParser
from mount import unmount_if_mounted, mount_if_unmounted

def do_hfs_filesystem_check(device_path):
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
        unmount_if_mounted(args.drive_path)
        do_hfs_filesystem_check(args.device_path)
        mount_if_unmounted(args.drive_path)
        
        print "\nFilesystem has been checked and re-mounted."

    except Exception as e:
        print "\n## Error : " % e
