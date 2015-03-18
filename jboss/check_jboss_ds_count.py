#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       JBOSS EAP DS Connection Count
Version     :       0.1
Author      :       Gurvinder
Summary     :       This program is a nagios plugin that check total active connection count for particular DS
Dependency  :       Linux/nagios/Python-2.6
 
Usage :
```````
shell> python check_jboss_ds_count.py
'''
 
#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
from optparse import OptionParser
import json
from requests.auth import HTTPDigestAuth
import requests
 
#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser

cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="jboss_host", help="JBOSS Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="jboss_port", help="JBOSS Server Port, e.g 9990")
cmd_parser.add_option("-u", "--user", type="string", action="store", dest="jboss_user", help="JBOSS Management User, e.g admin")
cmd_parser.add_option("-p", "--password", type="string", action="store", dest="jboss_pwd", help="JBOSS Management Password, e.g passw0rd")
cmd_parser.add_option("-t", "--dstype", type="string", action="store", dest="jboss_dstype", help="JBOSS Data Source Type, e.g data-source, xa-data-source")
cmd_parser.add_option("-n", "--dsname", type="string", action="store", dest="jboss_dsname", help="JBOSS Data Source Name, e.g ExampleDS")
cmd_parser.add_option("-w", "--warning", type="float", action="store", dest="jboss_warn", help="JBOSS DS active warning percentage, e.g 10")
cmd_parser.add_option("-c", "--critical", type="float", action="store", dest="jboss_critical", help="JBOSS DS active warning percentage, e.g 50")

#xa-data-source
(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.jboss_host and cmd_options.jboss_port and cmd_options.jboss_user and cmd_options.jboss_pwd and cmd_options.jboss_dstype and cmd_options.jboss_dsname and cmd_options.jboss_warn and cmd_options.jboss_critical):
    cmd_parser.print_help()
    sys.exit(3)


url = "http://"+cmd_options.jboss_user+":"+cmd_options.jboss_pwd+"@"+cmd_options.jboss_host+":"+cmd_options.jboss_port+"/management/subsystem/datasources/"+cmd_options.jboss_dstype+"/"+cmd_options.jboss_dsname+"/statistics/pool?"+urllib.urlencode({'include-runtime': 'true'})

try:
	r = requests.get(url,auth=HTTPDigestAuth(cmd_options.jboss_user, cmd_options.jboss_pwd))
except IOError:
	print "ERROR:JBOSS Not Reachable"
	sys.exit(3)
#print(url)
#sys.exit(0)
#print r
#print(r.url)
#print r.status_code
if r.status_code == 200:
	#print r.text
	data_string = json.loads(r.text)
	#print data_string
	#print data_string['ActiveCount']
	active_count = data_string['ActiveCount']
	#active_count = 1
	available_count = data_string['AvailableCount']
	#available_count = 20
	maxused_count = data_string['MaxUsedCount']
	active_count_p = 100 * float(active_count)/float(available_count)
	#print float(active_count_p)
	#sys.exit(0)
	if float(active_count_p) < float(cmd_options.jboss_warn) and float(active_count_p) >= 0:
		print "INFO:Active Count="+str(active_count)+", Available Count="+str(available_count)+", Max Used Count="+str(maxused_count)+"| active_count="+str(active_count)+", available_count="+str(available_count)+", maxused_count="+str(maxused_count)
		sys.exit(0)
	elif float(active_count_p) >= float(cmd_options.jboss_warn) and float(active_count_p) <= float(cmd_options.jboss_critical):
		print "WARNING:Active Count="+str(active_count)+", Available Count="+str(available_count)+", Max Used Count="+str(maxused_count)+"| active_count="+str(active_count)+", available_count="+str(available_count)+", maxused_count="+str(maxused_count)
		sys.exit(1)
	elif float(active_count_p) >= float(cmd_options.jboss_critical):
		print "CRITICAL:Active Count="+str(active_count)+", Available Count="+str(available_count)+", Max Used Count="+str(maxused_count)+"| active_count="+str(active_count)+", available_count="+str(available_count)+", maxused_count="+str(maxused_count)
		sys.exit(2)
	elif float(active_count_p) < 0:
		print "INVALID:Active Count="+str(active_count)+", Available Count="+str(available_count)+", Max Used Count="+str(maxused_count)+"| active_count="+str(active_count)+", available_count="+str(available_count)+", maxused_count="+str(maxused_count)
		sys.exit(3)	
else:
	data_string = json.loads(r.text)
	print "ERROR:HTTP RESPONSE CODE NOT 200, http_code="+str(r.status_code)+" Failure Description="+data_string['failure-description']
	sys.exit(3)
