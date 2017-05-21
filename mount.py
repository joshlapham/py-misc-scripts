#!/usr/bin/python

# import mount_cfg as cfg
from os import path
from subprocess import check_output

def unmount_if_mounted(drive_path):
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
            
def mount_smb_path(ip_address, remote_volume, local_volume_path, remote_username):
    cli = ['mount', '-t', 'smbfs',
           '//{}@{}/{}'.format(remote_username, ip_address, remote_volume),
           '{}'.format(local_volume_path)]
    
    # TODO: call `cli`
    
def check_if_volume_is_mounted(local_volume_path):
    # TODO: implement method
    pass
    
def make_mount_directory(local_volume_path):
    # TODO: implement method
    pass

if __name__ == '__main__':
    # TODO: use command line args (?)
    pass