#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check Index error count
Dependency  :       Linux/nagios/Python-2.6
Info 		: 		zero value means index is upto date. 
 
Usage :
```````
shell> python check_index_error_count.py
'''
 
#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
from xml.dom import minidom
from optparse import OptionParser
 
#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser

cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_host", help="SOLR Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="solr_port", help="SOLR Server Port, e.g 8080")
cmd_parser.add_option("-w", "--warning", type="long", action="store", dest="solr_warn", help="SOLR Index error count warning count, e.g 500")
cmd_parser.add_option("-c", "--critical", type="long", action="store", dest="solr_critical", help="SOLR Index error count critical count, e.g 1000")


(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.solr_host and cmd_options.solr_port and cmd_options.solr_warn and cmd_options.solr_critical):
    cmd_parser.print_help()
    sys.exit(3)

# set the locals
STATE=0 # the nagios return code, 0=OK, 1=WARN, 2=CRIT
STATENAME=dict()
STATENAME[0] = "OK"
STATENAME[1] = "WARNING"
STATENAME[2] = "CRITICAL"
STATENAME[3] = "UNKNOWN"

# Collect Solr Statistics Object
# http://localhost/report-alfresco.xml
#http://localhost:8080/solr/admin/cores?action=REPORT&wt=xml

class CollectStat:
    ''' Object to Collect the Statistics from the specified Element of the XML Data'''
    def __init__(self):
        self.stats = {}
url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/admin/cores?"+urllib.urlencode({'action': 'REPORT', 'wt': 'xml'})
#print(url)
try:
	response=urllib.urlopen(url).read()
except IOError:
	print "ERROR:Cannot connect to server"
	sys.exit(3)	
#print response
solr_all_stat = minidom.parseString(response)
#solr_all_stat = minidom.parseString(urllib.urlopen("https:///").read())
entries = solr_all_stat.getElementsByTagName('lst')
#print(len(entries)) #4 entries 
#print(entries[1].attributes['name'].value)
#print(entries[1].childNodes[0].toxml())
node = entries[1].childNodes[0]
node = node.childNodes
#print(node.length)
#print(node.item(16).toxml())
#print(node.item(16).nodeName)
#print(node.item(16).firstChild.data)
indexErrorCount = long(node.item(16).firstChild.data)
#print(indexErrorCount)

# get the data
solr_qps_stats = CollectStat()
if long(indexErrorCount)==0:
	print "INFO:No Issues with Index, Index error count= "+str(indexErrorCount)+"| i_err_count="+str(indexErrorCount)
	sys.exit(0)
elif long(indexErrorCount) >= long(cmd_options.solr_warn) and long(indexErrorCount) < long(cmd_options.solr_critical):
	print "WARNING:There is an issue with the index, Index error count = "+str(indexErrorCount)+"| i_err_count="+str(indexErrorCount)
	sys.exit(1)
elif long(indexErrorCount) >= long(cmd_options.solr_critical):
	print "CRITICAL:Invalid Index error count, Index error count = "+str(indexErrorCount)+"| i_err_count="+str(indexErrorCount)
	sys.exit(2)
elif long(indexErrorCount) < 0:
	print "UNKNOWN:Invalid Index error count, Index error count = "+str(indexErrorCount)+"| i_err_count="+str(indexErrorCount)
	sys.exit(3)	


