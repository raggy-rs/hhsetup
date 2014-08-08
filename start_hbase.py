#!/usr/bin/python
from reset import start_services
import os

def get_services():
        allservices = os.listdir('/etc/init.d')
        services = filter(lambda x: x.startswith('zookeeper'),allservices)
        services.extend(sorted(filter(lambda x: x.startswith('hbase'),allservices)))
        if not is_master() and 'hbase-master' in services:
                services.remove('hbase-master')
        return services

if __name__=='__main__':
	start_services(get_services())
