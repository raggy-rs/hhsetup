#!/usr/bin/python
import os,sys,shlex
import subprocess as sp
from settings import hosts

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def contains_any(whole, parts):
	for p in parts:
		if p in whole:
			return True
	return False

if __name__ == '__main__':
	ip = get_ip_address('eth0')

	if ip not in hosts:
		print 'There is no name configured for {} please add the ip and name into the hosts dict in settings.py'.format(ip)
		sys.exit(-1)
	sethostname='sudo hostname {}'.format(hosts[ip])
	sp.check_call(shlex.split(sethostname))
	with open('/etc/hostname','w') as out:
		out.write(hosts[ip])
	#sethostname='echo {}|sudo tee /etc/hostname'.format(hosts[ip])
	with open('/etc/hosts') as inp:
		etchosts=inp.readlines()
	etchosts=filter(lambda l: not contains_any(l,hosts.keys()),etchosts)
	for i,n in hosts.items():
		etchosts.append('{} {}\n'.format(i,n))
	with open('/etc/hosts','w') as out:
 		out.writelines(etchosts)

