#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check Count of missing transactions from the Index
Dependency  :       Linux/nagios/Python-2.6
Info 		    : 		  zero value means index is upto date. 
 
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


#url="http://localhost/report-alfresco.xml"
url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/admin/cores?"+urllib.urlencode({'action': 'REPORT', 'wt': 'xml'})
#print(url)

try:
	response=urllib.urlopen(url).read()
except IOError:
	print "ERROR:Cannot connect to server"
	sys.exit(3)

#print response
xmlResponse = minidom.parseString(response)
elements = xmlResponse.getElementsByTagName('lst')
#print(len(entries)) #4 entries 
#print(elements[2].attributes['name'].value) #output is alfresco
alfrescoElement = elements[2]
if alfrescoElement.getAttribute('name') != "alfresco":
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)

#print(alfrescoElement.getElementsByTagName('long'))
longElements = alfrescoElement.getElementsByTagName('long')

#ELEMENT API Reference https://docs.python.org/2/library/xml.dom.html#dom-element-objects
aclTransCountElement = "NULL"

for longElementSingle in longElements:
  #print longElementS.getAttribute('name')
  elementAttr = longElementSingle.getAttribute('name')
  if elementAttr=="Count of acl transactions in the index but not the DB":
    #print "Element Found"
    #print longElementSingle.getAttribute('name')
    aclTransCountElement = longElementSingle


if aclTransCountElement != "NULL":
  #print (indexTransCountElement.firstChild.data)
  indexCount = aclTransCountElement.firstChild.data
else:
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)

#print("Index Count = "+indexCount)
###########################################################################

#url="http://localhost/summary-alfresco.xml"
url = "http://"+cmd_options.solr_host+":"+cmd_options.solr_port+"/solr/admin/cores?"+urllib.urlencode({'action': 'summary', 'wt': 'xml'})
#print(url)

try:
	response=urllib.urlopen(url).read()
except IOError:
	print "ERROR:Cannot connect to server"
	sys.exit(3)

#print response
xmlResponse = minidom.parseString(response)
elements = xmlResponse.getElementsByTagName('lst')
#print(len(entries)) #4 entries 
#print(elements[2].attributes['name'].value) #output is alfresco
alfrescoElement = elements[2]
if alfrescoElement.getAttribute('name') != "alfresco":
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)

#print(alfrescoElement.getElementsByTagName('long'))
longElements = alfrescoElement.getElementsByTagName('long')

#ELEMENT API Reference https://docs.python.org/2/library/xml.dom.html#dom-element-objects
ApproxRemTransElement = "NULL" #Approx transactions remaining Element

for longElementSingle in longElements:
  #print longElementS.getAttribute('name')
  elementAttr = longElementSingle.getAttribute('name')
  if elementAttr=="Approx transactions remaining":
    #print "Element Found"
    #print longElementSingle.getAttribute('name')
    ApproxRemTransElement = longElementSingle


if ApproxRemTransElement != "NULL":
  #print (ApproxRemTransElement.firstChild.data)
  remain_trans = ApproxRemTransElement.firstChild.data
else:
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)
  
#print("Remaining Transactions = "+remain_trans)


if long(indexCount) == 0 and long(remain_trans) == 0:
	print("Index up to date, Remaining Transactions Count= "+str(remain_trans)+"|r_transactions="+str(remain_trans))
	sys.exit(0)

elif long(indexCount) > 0:
	if long(remain_trans) >= long(cmd_options.solr_warn) and long(remain_trans) < long(cmd_options.solr_critical):
		print("WARNING:Background indexing in progress, Remaining Transactions Count= "+str(remain_trans)+"|r_transactions="+str(remain_trans))
		sys.exit(1)
	elif long(remain_trans) > long(cmd_options.solr_critical):
		print("CLRITICAL:Missing Transactions, Remaining Transactions Count= "+str(remain_trans)+"|r_transactions="+str(remain_trans))
		sys.exit(2)
elif long(indexCount) < 0 or long(remain_trans)<0:
	print("UNKNOWN:Missing Transactions Status Unknown, Remaining Transactions Count= "+str(remain_trans))
	sys.exit(3)
		




