#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Project     :       Apache Solr Health Check
Version     :       1.0
Author      :       Gurvinder Dadyala
Summary     :       This program is a nagios plugin that check Index transaction count
Dependency  :       Linux/nagios/Python-2.6
Info 		: 		zero value means index is upto date. 
 
Usage :
```````
shell> python check_index_trans_count.py
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

cmd_parser = OptionParser(version="%prog 1.0")
cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_host", help="SOLR Server host, e.g locahost")
cmd_parser.add_option("-P", "--port", type="string", action="store", dest="solr_port", help="SOLR Server Port, e.g 8080")

(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.solr_host and cmd_options.solr_port):
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
indexTransCountElement = "NULL"

for longElementSingle in longElements:
  #print longElementS.getAttribute('name')
  elementAttr = longElementSingle.getAttribute('name')
  if elementAttr=="Index transaction count":
    #print "Element Found"
    #print longElementSingle.getAttribute('name')
    indexTransCountElement = longElementSingle


if indexTransCountElement != "NULL":
  #print (indexTransCountElement.firstChild.data)
  indexTransCount = indexTransCountElement.firstChild.data
else:
  print "UNKNOWN:Valid Tag not Found, Check XML response"
  sys.exit(3)


if long(indexTransCount)>=0:
	print "INFO:Index Transaction Count = "+str(indexTransCount)+"| i_trans_count="+str(indexTransCount)
	sys.exit(0)
else:
	print "ERROR:Invalid Index Transaction Count = "+str(indexTransCount)+"| i_trans_count="+str(indexTransCount)
	sys.exit(3)



