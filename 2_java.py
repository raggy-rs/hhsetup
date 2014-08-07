#!/usr/bin/python
import os,sys,shlex,tarfile
import subprocess as sp
from settings import jdktar, jvmdir, jdkversion 

if __name__ == '__main__':
	if not os.path.isfile(jdktar):
		print 'ERROR:',jdktar, "not found"
		sys.exit(1)
	if not os.path.exists(jvmdir):
		os.mkdir(jvmdir)
	if os.path.exists(jvmdir+jdkversion):
		print 'ERROR:',jvmdir+jdkversion ,'already exist'
		sys.exit(1)
	
	tar=tarfile.open(jdktar,'r:gz')
	tar.extractall(path=jvmdir)
	
	installstr='update-alternatives --install "/usr/bin/{0}" "{0}" "{1}{2}/bin/{0}" 1'
	sp.check_call(shlex.split(installstr.format('javac', jvmdir, jdkversion)))
	sp.check_call(shlex.split(installstr.format('java', jvmdir, jdkversion)))
	
	setstr='update-alternatives --set "{0}" "{1}{2}/bin/{0}"'
	sp.check_call(shlex.split(setstr.format('javac', jvmdir, jdkversion)))
	sp.check_call(shlex.split(setstr.format('java', jvmdir, jdkversion)))
	
	print sp.check_output(shlex.split('javac -version'))
	print sp.check_output(shlex.split('java -version'))
	sys.exit(0)
