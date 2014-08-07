#!/usr/bin/python
import os,sys,shlex
import subprocess as sp

if __name__=='__main__':
	if len(sys.argv)!=2 or sys.argv[1] not in ["master","slave"]:
		print 'USAGE:',sys.argv[0], "[master|slave]"
		sys.exit(1)
	master=sys.argv[1]=='master'
	text = '''deb [arch=amd64] http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh precise-cdh5 contrib 
deb-src http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh precise-cdh5 contrib'''

	with open('/etc/apt/sources.list.d/cloudera.list','w') as out:
		out.write(text)

	key=sp.check_output(shlex.split('curl -s http://archive.cloudera.com/cdh5/ubuntu/precise/amd64/cdh/archive.key'))
 	p=sp.Popen(shlex.split('apt-key add -'), stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)
	out,err = p.communicate(input=key)
	print out,err
	
	sp.check_call(shlex.split('apt-get update'))
	sp.check_call(shlex.split('apt-get install zookeeper'))
	if master:
		sp.check_call(shlex.split('apt-get install hadoop-yarn-resourcemanager hadoop-hdfs-namenode'))
		sp.check_call(shlex.split('apt-get install hbase-master'))
	else:
		sp.check_call(shlex.split('apt-get install hadoop-yarn-nodemanager hadoop-hdfs-datanode hadoop-mapreduce'))
	sp.check_call(shlex.split('apt-get install  hadoop-client'))
	sp.check_call(shlex.split('apt-get install hbase hbase-regionserver'))
