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
	datapath=os.path.expanduser('~/data')
	nnpath=os.path.join(datapath,'/dfs/nn')
	dnpath=os.path.join(datapath,'/dfs/dn')
	if not os.path.isdir(nnpath):
		os.makedirs(nnpath)
	if not os.path.isdir(dnpath):
		os.makedirs(dnpath)
	
	call('chown -R hdfs:hdfs '+datapath)
