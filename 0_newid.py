#!/usr/bin/python
import os,sys,shlex,stat
import subprocess as sp
from settings import sshdir,rsafile

if __name__ == '__main__':
	if not os.path.isdir(sshdir):
		os.mkdir(sshdir)
		os.chmod(sshdir, stat.S_IRWXU)
	keygenstr='ssh-keygen -t rsa -f {}{} -N ""'.format(sshdir,rsafile)
	print sp.check_output(shlex.split(keygenstr))
	addkeystr="cat {0}{}.pub >> {0}authorized_keys".format(sshdir,rsafile)
	print sp.check_output(shlex.split(addkeystr))

