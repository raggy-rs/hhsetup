#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import username, masterip, configname, hosts

def call(cmdstr):
	sp.check_call(shlex.split(cmdstr))

if __name__ == '__main__':
	masterhost = hosts[masterip]
	print 'Update Alternatives'
        scpstr = 'scp -r {0}@{1}:/etc/hadoop/conf.{2} /etc/hadoop/'.format(username, masterhost, configname)
	installalt = 'update-alternatives --install /etc/hadoop/conf hadoop-conf /etc/hadoop/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hadoop-conf /etc/hadoop/conf.{}'.format(configname)
	print 'Copy {0}@{1}:/etc/hadoop/conf.{2} to /etc/hadoop/'.format(username, masterhost, configname)
	call(scpstr)
	call(installalt)
	call(setalt)
        
	scpstr='scp -r {0}@{1}:/etc/hbase/conf.{2} /etc/hbase/'.format(username, masterhost, configname)
	installalt = 'update-alternatives --install /etc/hbase/conf hbase-conf /etc/hbase/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hbase-conf /etc/hbase/conf.{}'.format(configname)
	print 'Copy {0}@{1}:/etc/hbase/conf.{2} to /etc/hbase/'.format(username, masterhost, configname)
	call(scpstr)
	call(installalt)
	call(setalt)
	print 'Create data directories if nessecary'
	datapath=os.path.expanduser('~/data')
	nnpath=os.path.join(datapath,'/dfs/nn')
	dnpath=os.path.join(datapath,'/dfs/dn')
	if not os.path.isdir(nnpath):
		os.makedirs(nnpath)
	if not os.path.isdir(dnpath):
		os.makedirs(dnpath)
	
	call('chown -R hdfs:hdfs '+datapath)
