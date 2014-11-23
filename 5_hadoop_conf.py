#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import username, masterip, configname, hosts

def call(cmdstr):
	sp.check_call(shlex.split(cmdstr))

if __name__ == '__main__':
	confbase = os.path.expanduser('~/hhsetup/conf/')
	print 'Update Alternatives',
	for what in ['hadoop','hbase','zookeeper']:
		print what,
		confdir = os.path.join(confbase,what)
		call('update-alternatives --install /etc/{0}/conf {0}-conf {1} 100'.format(what,confdir))
		call('update-alternatives --set {0}-conf {1}'.format(what, confdir))
        
	print '\nCreate data directories if nessecary'
	datapath='/mnt/data/'
	nnpath=os.path.join(datapath,'dfs/nn')
	dnpath=os.path.join(datapath,'dfs/dn')
	logpath = os.path.join(datapath,'log')
	if not os.path.isdir(nnpath):
		os.makedirs(nnpath)
	if not os.path.isdir(dnpath):
		os.makedirs(dnpath)
	if not os.path.isdir(logpath):
		os.makedirs(logpath)
	call('chown -R hdfs:hadoop '+datapath)
	call('chmod g+w '+datapath)
	call('usermod -a -G hadoop hbase')
	print 'Add HADOOP_CLASSPATH to .bashrc'
	with open(os.path.expanduser('~/.bashrc'),'aw') as out:
		out.write("export HADOOP_CLASSPATH=`hbase classpath`/home/cloud/hhsetup/jar/*:")
