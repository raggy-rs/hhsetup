#!/usr/bin/python
import os,sys,shlex,stat
import subprocess as sp
from settings import username,masterip,sshdir,rsafile

if __name__ == '__main__':
        if not os.path.isdir(sshdir):
                os.mkdir(sshdir)
                os.chmod(sshdir,stat.S_IRWXU)
	scpstr='scp {0}@{1}:{2}{3}* {2}'.format(username,masterip,sshdir,rsafile) 
	print scpstr
        print sp.check_output(shlex.split(scpstr))
	
	addkeystr="ssh-copy-id -i {0}{1}.pub localhost".format(sshdir,rsafile)
        print sp.check_output(shlex.split(addkeystr))
