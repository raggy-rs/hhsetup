#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import username, masterip, configname

if __name__ == '__main__':
        scpstr='scp -r {0}@{1}:/etc/hadoop/conf.{2} /etc/hadoop/'.format(username,masterip,configname)
	installalt = 'update-alternatives --install /etc/hadoop/conf hadoop-conf /etc/hadoop/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hadoop-conf /etc/hadoop/conf.{}'.format(configname)
	print 'Copy {0}@{1}:/etc/hadoop/conf.{2} to /etc/hadoop/'.format(username,masterip,configname)
	sp.check_call(shlex.split(scpstr))
	print 'Update Alternatives'
	sp.check_call(shlex.split(installalt))
	sp.check_call(shlex.split(setalt))
	print 'Create data directories if nessecary'
	nnpath=os.path.expanduser("~/data/dfs/nn")
	dnpath=os.path.expanduser("~/data/dfs/dn")
	if not os.path.isdir(nnpath):
		os.makedirs(nnpath)
	if not os.path.isdir(dnpath):
		os.makedirs(dnpath)
