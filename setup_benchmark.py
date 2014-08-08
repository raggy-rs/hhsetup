#!/usr/bin/python
import os, shlex, subprocess
def call(argstr):
        subprocess.check_call(shlex.split(argstr))

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


if __name__=='__main__':
	kmers = [8,16,32]
	create_tables(kmers)
