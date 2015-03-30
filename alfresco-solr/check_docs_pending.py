#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check docs pending
Dependency  :       Linux/nagios/Python-2.6
 
Usage :
```````
shell> python check_docs_pending.py
'''
 
#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
import xml.etree.ElementTree as ET
from optparse import OptionParser
 
#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser

cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_host", help="SOLR Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="solr_port", help="SOLR Server Port, e.g 8080")
cmd_parser.add_option("-w", "--warning", type="long", action="store", dest="solr_warn", help="SOLR docs pending warning count, e.g 10")
cmd_parser.add_option("-c", "--critical", type="long", action="store", dest="solr_critical", help="SOLR docs pending critical count, e.g 100")


(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.solr_host and cmd_options.solr_port and cmd_options.solr_warn and cmd_options.solr_critical):
    cmd_parser.print_help()
    sys.exit(3)

class CollectStat:
    ''' Object to Collect the Statistics from the specified Element of the XML Data'''
    def __init__(self):
		self.stats = {}
		url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/alfresco/admin/stats.jsp"
		#print(url)
		try:
			doc = ET.fromstring(urllib.urlopen(url).read())
		except IOError:
			print "ERROR:Cannot connect to server"
			sys.exit(3)
		groupname = "CORE"
		entryname = "updateHandler"
		#print doc
		tags = doc.findall(".//solr-info/UPDATEHANDLER/entry")
		for b in tags:
			if b.find('name').text.strip() == entryname:
				stats = b.findall("stats/*")
				for stat in stats:
					self.stats[stat.get('name')] = stat.text.strip()
					
						
solr_qps_stats = CollectStat()
#print solr_qps_stats.stats
#print solr_qps_stats.stats['docsPending']
docsPending = solr_qps_stats.stats['docsPending']
if long(docsPending) == 0:
	print "OK: No Indexing going on,docsPending = "+docsPending+"| d_pending_count="+str(docsPending)
	sys.exit(0)
elif long(docsPending) >= long(cmd_options.solr_warn) and long(docsPending) < long(cmd_options.solr_critical):
	print "WARNING: Index is in progress,docsPending = "+docsPending+"| d_pending_count="+str(docsPending)
	sys.exit(1)
elif long(docsPending) >= long(cmd_options.solr_critical):
	print "CRITICAL: Index is in progress,docsPending = "+docsPending+"| d_pending_count="+str(docsPending)
	sys.exit(2)
elif long(docsPending) < 0:
	print "UNKNOWN: Invalid indexing status,docsPending = "+docsPending+"| d_pending_count="+str(docsPending)
	sys.exit(3)			





