#!/usr/bin/python
from reset import start_services,get_services

if __name__=='__main__':
	services = get_services()
	services = filter(lambda x: "hbase" in x, services)
	start_services(get_services())

