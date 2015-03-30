#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check Count of missing transactions from the Index
Dependency  :       Linux/nagios/Python-2.6
Info 		: 		zero value means index is upto date. 
 
Usage :
```````
shell> python check_solr_index.py
'''
 
#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
from xml.dom import minidom
from optparse import OptionParser
import xml.etree.ElementTree as ET
 
#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser

cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_host", help="SOLR Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="solr_port", help="SOLR Server Port, e.g 8080")
cmd_parser.add_option("-w", "--warning", type="long", action="store", dest="solr_warn", help="SOLR remaining transaction warning count, e.g 500")
cmd_parser.add_option("-c", "--critical", type="long", action="store", dest="solr_critical", help="SOLR remaining transaction critical count, e.g 1000")

(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.solr_host and cmd_options.solr_port and cmd_options.solr_warn and cmd_options.solr_critical):
    cmd_parser.print_help()
    sys.exit(3)

url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/admin/cores?"+urllib.urlencode({'action': 'REPORT', 'wt': 'xml'})
#print(url)

try:
	response=urllib.urlopen(url).read()
except IOError:
	print "ERROR:Cannot connect to server"
	sys.exit(3)

#print response
root = ET.fromstring(response)
#print root
elements = root.findall(".//*[@name='alfresco']")
element = elements[0].findall("./long[@name='Count of acl transactions in the index but not the DB']")
#print len(element)

#indexCount  = <long name="Count of acl transactions in the index but not the DB">0</long>
#remain_trans = <long name="Approx transactions remaining">0</long>

if not element:
  #print "element (Count of acl transactions in the index but not the DB) not found"
  indexCount = "NULL"
else:
  #print element[0]
  #print element[0].text
  #print element[0].tag
  #print element[0].attrib
  indexCount = element[0].text
  
#Fetching data from anorther URL 
##summary_url="http://192.168.100.243:8080/solr/admin/cores?action=summary&wt=xml"
summary_url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/admin/cores?"+urllib.urlencode({'action': 'summary', 'wt': 'xml'})
#print(summary_url)
try:
	response_1=urllib.urlopen(summary_url).read()
except IOError:
	print "ERROR:Cannot connect to server"
	sys.exit(3)
#print response
root_1 = ET.fromstring(response_1)
#print root
elements_1 = root_1.findall(".//*[@name='alfresco']")
element_1 = elements_1[0].findall("./long[@name='Approx transactions remaining']")
#print len(element)

if not element_1:
  #print "Element (Approx transactions remaining) not found"
  remain_trans = "NULL"
else:
  #print element_1[0]
  #print element_1[0].text
  #print element_1[0].tag
  #print element_1[0].attrib
  remain_trans = element_1[0].text


if str(indexCount) == "NULL" or str(remain_trans) == "NULL":
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)
elif long(indexCount) == 0 and long(remain_trans) == 0:
	print("Index is up to date, Remaining Transactions Count= "+str(remain_trans)+"|r_transactions="+str(remain_trans))
	sys.exit(0)
elif long(indexCount) > 0:
	if long(remain_trans) >= long(cmd_options.solr_warn) and long(remain_trans) < long(cmd_options.solr_critical):
		print("Warning:Background indexing in progress, Remaining Transactions Count= "+str(remain_trans)+"|r_transactions="+str(remain_trans))
		sys.exit(1)
	elif long(remain_trans) >= long(cmd_options.solr_critical):
		print("Critical|Missing Transactions, Remaining Transactions Count= "+str(remain_trans)+"|m_transactions="+str(remain_trans))
		sys.exit(2)
elif long(indexCount) < 0 or long(remain_trans)<0:
	print("Missing Transactions Status Unknown, Remaining Transactions Count= "+str(remain_trans))
	sys.exit(3)
		




