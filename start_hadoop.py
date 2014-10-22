#!/usr/bin/python
from reset import start_services,get_services

if __name__=='__main__':
	services = get_services()
	services = filter(lambda x: "hbase" not in x and 'zookeeper' not in x, services)
	print services
	start_services(services)
