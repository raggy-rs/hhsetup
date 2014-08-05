#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import username, masterip, configname

if __name__ == '__main__':
        scpstr='scp -r {0}@{1}:/etc/hadoop/conf.{2} /etc/hadoop/conf.{2}'.format(username,masterip,configname)
	installalt = 'update-alternatives --install /etc/hadoop/conf hadoop-conf /etc/hadoop/conf.{} 50'.format(configname)
	setalt = 'update-alternatives --set hadoop-conf /etc/hadoop/conf.{}'.format(configname)
	sp.check_call(shlex.split(scpstr))
	sp.check_call(shlex.split(installalt))
	sp.check_call(shlex.split(setalt))
	os.makedirs(os.path.expanduser("~/data/dfs/nn"))
	os.mkdir(os.path.expanduser("~/data/dfs/dn"))
