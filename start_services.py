#!/usr/bin/python
import os,sys,shlex
import subprocess as sp

#for x in `cd /etc/init.d ; ls hadoop-hdfs-*` ; do sudo service $x start ; done
if __name__ == '__main__':
	services = os.listdir('/etc/init.d')
	services = filter(lambda x: x.startswith("hadoop"),services)
	for service in services:
		startcmd="service {} start".format(service)
		sp.check_call(shlex.split(startcmd))		

