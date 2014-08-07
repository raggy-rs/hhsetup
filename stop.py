#!/usr/bin/python
from reset import stop_services,get_services

if __name__=='__main__':
	stop_services(get_services())
