#!/usr/bin/python
import os, shlex
import subprocess as sp
from settings import username

def call(argstr):
	sp.check_call(shlex.split(argstr))

def clean_dir(directory):
	if os.path.isdir(directory):
		for f in os.listdir(directory):
			call('rm -r '+os.path.join(directory,f))

def clear_data_dirs():
	clean_dir('/var/lib/zookeeper')
	clean_dir('/mnt/data/dfs/dn')
	clean_dir('/mnt/data/dfs/nn')

def clear_log_dirs():
	logbase='/var/log'
	logdirs=os.listdir(logbase)
	for d in logdirs:
		if d.startswith('hadoop') or d in ['hbase', 'zookeeper']:
			logdir = os.path.join(logbase,d)
			for f in os.listdir(logdir):
				p=os.path.join(logdir,f)
				if os.path.isfile(p):
					os.remove(p)

def format_namenode():
	call('sudo -u hdfs hadoop namenode -format')

def init_zookeeper():
	call('service zookeeper-server init --force --myid=1')

def stop_services(services):
	for service in reversed(services):
		call("service {} stop".format(service))		

def init_hdfs():
	#start_services(["hadoop-hdfs-namenode"])
	call('sudo -u hdfs hadoop fs -mkdir /hbase')
	call('sudo -u hdfs hadoop fs -chown hbase:hbase /hbase')
	call('sudo -u hdfs hadoop fs -mkdir /tmp')
	call('sudo -u hdfs hadoop fs -chmod -R 1777 /tmp')
	call('sudo -u hdfs hadoop fs -mkdir -p /user/cloud')
	call('sudo -u hdfs hadoop fs -chown cloud:cloud /user/cloud')

def list_running_services():
	print 'This processes were succesfully started'
        javahome = '/usr/lib/jvm/jdk1.7.0_45'
        call(os.path.join(javahome,'bin/jps'))

def start_services(services):
	for service in services:
		call("service {} start".format(service))
	list_running_services()

def get_services():
	if is_master():
		services = ['hadoop-hdfs-namenode', 'hadoop-yarn-resourcemanager', 'zookeeper-server', 'hbase-master']

	else:
		services = ['hadoop-hdfs-datanode', 'hadoop-yarn-nodemanager', 'hbase-regionserver']
	return services

def is_master():
	import socket, settings
	return settings.hosts[settings.masterip]==socket.gethostname() 

if __name__ == '__main__':
	services=get_services()
	print services
	stop_services(services)
	clear_data_dirs()
	clear_log_dirs()
	if is_master():
		format_namenode()
		init_zookeeper()
		init_hdfs()
