#!/usr/bin/python
from glob import glob
from os.path import basename
from subprocess import check_output,check_call
import shlex
import time
from argparse import ArgumentParser
from align import get_libjars

align_jar = "gblast-align-0.8.0-SNAPSHOT.jar"
import_jar = "gblast-importer-0.8.0-SNAPSHOT.jar"
common_jar = "gblast-common-0.8.0-SNAPSHOT.jar"

benchmark_input = "data/compare.txt"
hdfs_data_path = "hdfs:///user/cloud/data/"
log_file = "benchmark."+time.strftime("%d.%m_%H:%M")+".log"

def get_db_size():
	output=check_output("hadoop fs -du /hbase",shell=True)
	print output
	line = filter(lambda line: line.endswith("data"), output.split("\n"))[0]
	return int(line.split()[0])

def measure_time(cmd,*args):
	print args
	begin = time.clock()
	cmd(*args)
	return time.clock()-begin

def run_import(files,k):
	files = ",".join(map(lambda f: hdfs_data_path+f, files))
	cmd = "hadoop jar jar/{} -libjars jar/{} -f {} -k {} -v".format(import_jar,common_jar,files,k)
	check_call(cmd,shell=True)

def run_align(query,k):
	cmd = "hadoop jar jar/{} {} -i {} -f {} -k {}".format(align_jar,get_libjars(),query,hdfs_data_path+query,k)
	check_call(cmd,shell=True);

def log(formatstr,*values):
	with open(log_file,"a") as out:
		output = formatstr.format(*values)
		print output
		out.write(output)

if __name__=="__main__":
	with open(benchmark_input) as inp:
		lines=inp.readlines()
	lineparser = ArgumentParser()
	lineparser.add_argument("query",type=str)
	lineparser.add_argument("-k",type=int)
	lineparser.add_argument("-db",type=str, nargs="+")
	for line in lines:
		line = line.strip().lstrip()
		if not line.startswith("#") and line != "":
			args = lineparser.parse_args(shlex.split(line))
			log("size {}\n",get_db_size())
			log("import {} {} time {}\n",args.db,args.k,measure_time(run_import,args.db,args.k))
			log("size {}\n",get_db_size())
			log("align {} {} time {}\n",args.query,args.k,measure_time(run_align,args.query,args.k))
