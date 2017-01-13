#!/usr/bin/python

from subprocess import Popen, PIPE, call

def _do_command_as_process(cli):
    p = Popen(cli, shell=False, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    
    if p.returncode == 0:
        return stdout
    else:
        raise StandardError(str(stderr))
        
def _do_command(cli):
    call(cli)
    
def do_command(cli, own_process=False):
    if own_process is True:
        _do_command_as_process(cli)
    else:
        _do_command(cli)
        
if __name__ == '__main__':
    pass