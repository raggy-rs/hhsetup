#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import username, masterip, configname, hosts

if __name__ == '__main__':
	masterhost = hosts[masterip]
	print 'Update Alternatives'
        scpstr = 'scp -r {0}@{1}:/etc/hadoop/conf.{2} /etc/hadoop/'.format(username, masterhost, configname)
	installalt = 'update-alternatives --install /etc/hadoop/conf hadoop-conf /etc/hadoop/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hadoop-conf /etc/hadoop/conf.{}'.format(configname)
	print 'Copy {0}@{1}:/etc/hadoop/conf.{2} to /etc/hadoop/'.format(username, masterhost, configname)
	sp.check_call(shlex.split(scpstr))
	sp.check_call(shlex.split(installalt))
	sp.check_call(shlex.split(setalt))
        
	scpstr='scp -r {0}@{1}:/etc/hbase/conf.{2} /etc/hbase/'.format(username, masterhost, configname)
	installalt = 'update-alternatives --install /etc/hbase/conf hbase-conf /etc/hbase/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hbase-conf /etc/hbase/conf.{}'.format(configname)
	print 'Copy {0}@{1}:/etc/hbase/conf.{2} to /etc/hbase/'.format(username, masterhost, configname)
	sp.check_call(shlex.split(scpstr))
	sp.check_call(shlex.split(installalt))
	sp.check_call(shlex.split(setalt))
	print 'Create data directories if nessecary'
	nnpath=os.path.expanduser("~/data/dfs/nn")
	dnpath=os.path.expanduser("~/data/dfs/dn")
	if not os.path.isdir(nnpath):
		os.makedirs(nnpath)
	if not os.path.isdir(dnpath):
		os.makedirs(dnpath)
