#!/usr/bin/python
import os, shlex, subprocess, time

def call(argstr, shell=False):
        subprocess.check_call(shlex.split(argstr),shell=shell)

def create_tables(kmers):
	script='create "METAINFO", "d"\ncreate "SEQUENCE", "d"\n'
	for k in kmers:
		script += 'create "KMERS{}", "m", "d"\n'.format(k)
	script += 'list\nexit\n'
	scriptfile = 'setup_hbase.rb'
	print 'FILE:',scriptfile
	print script
	with open(scriptfile,"w") as out:
		out.write(script)
	call('hbase shell '+scriptfile)

def copy_data():
	call('hadoop fs -mkdir -p /user/cloud/data/')
	call('hadoop fs -copyFromLocal /home/cloud/hhsetup/data/* /user/cloud/data/',True)

if __name__=='__main__':
	kmers = [8,16,32]
	create_tables(kmers)
	copy_data()
