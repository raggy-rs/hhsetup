#!/usr/bin/python
from glob import glob
from os.path import basename
from subprocess import check_output,check_call,Popen,PIPE
import shlex
import timeit
import time
from argparse import ArgumentParser
from align import get_libjars
from StringIO import StringIO

align_jar = "gblast-align-0.8.0-SNAPSHOT.jar"
import_jar = "gblast-importer-0.8.0-SNAPSHOT.jar"
common_jar = "gblast-common-0.8.0-SNAPSHOT.jar"

hbase_conf = "-conf conf/hbase/hbase-site.xml"
libjars = get_libjars()

benchmark_input = "data/compare.txt"
hdfs_data_path = "hdfs:///user/cloud/data/"
log_file = "benchmark."+time.strftime("%d.%m_%H:%M")+".log"

def get_db_size():
	output=check_output("hadoop fs -du /hbase",shell=True)
	print output
	line = filter(lambda line: line.endswith("data"), output.split("\n"))[0]
	return int(line.split()[0])

def truncate_db():
	check_call("hbase shell truncate_hbase.rb",shell=True)

def log_output_and_time(cmd,*args):
	begin = timeit.default_timer()
	log("command:\n{}\nparameters:\n{}\n", cmd.__name__, ", ".join(map(str,args)))
	log("output:\n{}\ntime:\n{}\n", cmd(*args), timeit.default_timer()-begin)

def run_import(files,k):
	files = ",".join(map(lambda f: hdfs_data_path+f, files))
	cmd = "hadoop jar jar/{} -libjars jar/{} {} -f {} -k {} -v".format(import_jar, common_jar, hbase_conf, files, k)
	output=StringIO()
	process = Popen(cmd,shell=True,stdout=PIPE)
	process.wait()
	return process.stdout.read()

def run_align(query,k, x):
	if x:
		x="-x"
	cmd = "hadoop jar jar/{} {} {} -i {} -f {} -k {} -v {}".format(align_jar, libjars, hbase_conf, query, hdfs_data_path+query, k, x)
	output=StringIO()
	process = Popen(cmd,shell=True,stdout=PIPE);
	process.wait()
	return process.stdout.read()

def log(formatstr,*values):
	with open(log_file,"a") as out:
		output = formatstr.format(*values)
		print "LOG:",output
		out.write(output)

if __name__=="__main__":
	with open(benchmark_input) as inp:
		lines=inp.readlines()
	lineparser = ArgumentParser()
	lineparser.add_argument("query",type=str)
	lineparser.add_argument("-k",type=int)
	lineparser.add_argument("-db",type=str, nargs="+")
	lineparser.add_argument("-x",action="store_true")
	for line in lines:
		line = line.strip().lstrip()
		if not line.startswith("#") and line != "":
			args = lineparser.parse_args(shlex.split(line))
			log_output_and_time(get_db_size)
			log_output_and_time(run_import,args.db,args.k)
			log_output_and_time(get_db_size)
			log_output_and_time(run_align,args.query,args.k,args.x)
			#log_output_and_time(get_db_size)
			log_output_and_time(truncate_db)

