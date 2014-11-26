#!/usr/bin/python
import os, shlex, subprocess, time

def call(argstr, shell=False):
        subprocess.check_call(shlex.split(argstr),shell=shell)

def create_tables(kmers):
	script='create "METAINFO", "d"\n'#\ncreate "SEQUENCE", "d"\n'
	#for k in kmers:
	#	script += 'create "KMERS{}", "m", "d"\n'.format(k)
	script += 'list\nexit\n'
	scriptfile = 'setup_hbase.rb'
	print 'FILE:',scriptfile
	print script
	with open(scriptfile,"w") as out:
		out.write(script)
	call('hbase shell '+scriptfile)
	for k in kmers:
		call('hbase org.apache.hadoop.hbase.util.RegionSplitter KMERS{} UniformSplit -c 4 -f d'.format(k))

def copy_data():
	subprocess.check_call('hadoop fs -mkdir -p /user/cloud/data/',shell=True)
	subprocess.check_call('hadoop fs -copyFromLocal /home/cloud/hhsetup/data/* /user/cloud/data/',shell=True)

if __name__=='__main__':
	kmers = [8,16,32]
	create_tables(kmers)
	copy_data()
