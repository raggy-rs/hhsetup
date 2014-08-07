#!/usr/bin/python
import os,sys,shlex,shutil
import subprocess as sp

#for x in `cd /etc/init.d ; ls hadoop-hdfs-*` ; do sudo service $x start ; done
services = ['hadoop-hdfs-namenode','hadoop-yarn-resourcemanager','hbase-master','hbase-regionserver']

def call(argstr):
	sp.check_call(shlex.split(argstr))

def clear_log_dirs():
	logbase='/var/log'
	logdirs=os.listdir(logbase)
	for d in logdirs:
		if d.startswith('hadoop') or d.startswith('hbase'):
			logdir = os.path.join(logbase,d)
			for f in os.listdir(logdir):
				os.remove(os.path.join(logdir,f))

def format_namenode():
	call('sudo -u hdfs hadoop namenode -format')

def stop_services(services):
	for service in reversed(services):
		call("service {} stop".format(service))		

def start_services(services):
	for service in services:
		call("service {} start".format(service))
		if service=='hadoop-hdfs-namenode':
			call('sudo -u hdfs hadoop fs -mkdir /hbase')
			call('sudo -u hdfs hadoop fs -chown hbase:hbase /hbase')


if __name__ == '__main__':
	allservices = os.listdir('/etc/init.d')
	services = filter(lambda x: x.startswith("hadoop-hdfs"),allservices)
	services.extend(filter(lambda x: x.startswith('hadoop-yarn'),allservices))
	services.extend(filter(lambda x: x.startswith('zookeeper'),allservices))
	services.extend(sorted(filter(lambda x: x.startswith('hbase'),allservices)))
	print services
	stop_services(services)
	clear_log_dirs()
	format_namenode()
	start_services(services)

