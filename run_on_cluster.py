#!/usr/bin/python
import sys, os
from reset import call
from settings import hosts

def run_on_cluster(scriptname):
	if scriptname[-3:]!='.py':
		print 'Only runs python scripts'
		return
	scriptdir = '/home/cloud/hhsetup'
	script = os.path.join(scriptdir, name)
	print scriptdir, os.path.dirname(script)
	if os.path.dirname(script) != scriptdir:
		print 'Script must be in', scriptdir
		return
	for node in sorted(hosts.values()):
		print 'call {} on {}'.format (script,node)
		call('ssh root@{} "{}"'.format(node, script))
	print sorted(hosts.values())

if __name__ == '__main__':
	args=sys.argv
	if len(args) > 1:
		for name in args[1:]:
			run_on_cluster(name)
