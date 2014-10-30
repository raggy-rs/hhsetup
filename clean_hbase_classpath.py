#!/usr/bin/python
import subprocess as sp
import os
import glob

classpath=[]
paths = set([os.path.dirname(os.path.abspath(x)) for x in sp.check_output(["hbase","classpath"]).split(':')])

for p in paths:
	jars=glob.glob(p+'/*.jar')
	if len(jars)>0:
		classpath+=jars
	else:
		classpath+=[p]
classpath+=['/etc/hbase/']
print ':'.join(classpath)
	
