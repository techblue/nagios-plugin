#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check Solr status
Dependency  :       Linux/nagios/Python-2.6
 
Usage :
```````
shell> python check_solr_ping.py
'''
 
#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
from optparse import OptionParser
import json
 
#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser

cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_host", help="SOLR Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="solr_port", help="SOLR Server Port, e.g 8080")
#cmd_parser.add_option("-w", "--warning", type="long", action="store", dest="solr_warn", help="SOLR index warning count, e.g 500")
#cmd_parser.add_option("-c", "--critical", type="long", action="store", dest="solr_critical", help="SOLR index critocal count, e.g 1000")

(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.solr_host and cmd_options.solr_port):
    cmd_parser.print_help()
    sys.exit(3)

url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/alfresco/admin/ping"
#print(url)
try:
	response=urllib.urlopen(url).read()
except IOError:
	print "ERROR:Solr Not Reachable"
	sys.exit(3)

#print response
data_string = json.loads(response)
#print data_string['status']
solr_status = data_string['status']


if solr_status == 'OK':
	print("INFO:Solr Instance Running")
	sys.exit(0)
elif solr_status != 'OK':
	print("UNKNOWN:Solr Instance Status Unknown")
	sys.exit(3)



