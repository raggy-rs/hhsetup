#!/usr/bin/python
from reset import start_services,call
import os

def get_services():
        allservices = os.listdir('/etc/init.d')
        services = filter(lambda x: x.startswith("hadoop-hdfs"),allservices)
        services.extend(filter(lambda x: x.startswith('hadoop-yarn'),allservices))
        return services

if __name__=='__main__':
	start_services(get_services())
