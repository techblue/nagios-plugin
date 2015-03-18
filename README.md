Overview
===================
Documentation include details of six Nagios plugin for checking Solr health and JBoss datasource connection pool count plugin.
List of plugins is as follows
----------
> - check_count_dup_tran.py
> - check_index_error_count.py
> - check_solr_missing_trans.py
> - check_docs_pending.py
> - check_index_trans_count.py
> - check_solr_ping.py
> - check_jboss_ds_count.py

We will discussing each plugin in the following section. In order to run SOLR plugins in Alfresco, user will have make configuration changes for running Solr on 8080 port. Refer to [document](./nagios_alfreco_configuration_changes.odt) for running Solr on 8080 port.

Plugin Details
-----------------
**check_count_dup_tran.py**
This plugin provides information related count of duplicate transactions in Solr Alfresco Core indexes. It indicates the number of transactions that appear more than once in the index. The value of this parameter should be zero. If not, there is an issue with the index. Plugin accepts four parameters as follows
> - Host - IP of Solr server
> - Port - Port of Solr server 
> - Warning count - Duplicate transaction warning count
> - Critical count - Duplicate transaction critical count

**Example**

    check_count_dup_tran.py -H 127.0.0.1 -P 8080 -w 10 -c 100

**Output**

    INFO:No Issues with Index, Duplicate transaction count in index = 0| dup_trans_count=0

**check_index_error_count.py**
This plugin provides information related to counts of error documents in the index. It is used to mark nodes that failed to be indexed. If the value of this parameter is not zero, then there is an issue with the index. Plugin accepts four parameters as follows
> - Host - IP of Solr server
> - Port - Port of Solr server 
> - Warning count - Index error warning count
> - Critical count - Index error critical count

**Example**

    check_index_error_count.py -H 127.0.0.1 -P 8080 -w 10 -c 100

**Output**

    INFO:No Issues with Index, Index error count= 0| i_err_count=0

**check_solr_missing_trans.py**
This plugin provides information related to count of missing transactions from the database. It indicates the number of transactions in the database but not in the index. The value of this index should be zero when the index is up-to-date. It accepts four parameters as follows
> - Host - IP of Solr server
> - Port - Port of Solr server 
> - Warning count – Warning count of missing transactions
> - Critical count – Critical count of missing transactions

**Example**

    check_solr_missing_trans.py -H 127.0.0.1 -P 8080 -w 10 -c 100

**Output**

    Index is up to date

**check_index_trans_count.py**
This plugin provides number of transactions count in the index. It does not have warning or critical levels because the output is for statistics only. It accepts only 2 parameters
> - Host - IP of Solr server
> - Port - Port of Solr server 

**Example**

    check_index_trans_count.py -H 127.0.0.1 -P 8080

**Output**

    INFO:Index Transaction Count = 15| i_trans_count=15


**check_solr_ping.py**
This plugin indicates whether Solr is active or not. It only accepts two parameters
> - Host - IP of Solr server
> - Port - Port of Solr server

**Example**

    check_solr_ping.py -H 127.0.0.1 -P 8080

**Output**

    INFO:Solr Instance Running

**check_docs_pending.py**
This plugin indicates status of documents getting re-indexed. Value of this plugin should be zero if there is no re-indexing going on otherwise output will show number of documents already processed while re-indexing routine. It takes four parameters.
> - Host - IP of Solr server
> - Port - Port of Solr server
> - Warning count - Documents pending warning count
> - Critical count - Documents pending critical count

**Example**

    check_docs_pending.py -H 127.0.0.1 -P 8080 -w 10 -c 100

**Output**

    OK: No Indexing going on,docsPending = 0| d_pending_count=0

**check_docs_pending.py**
This Jboss plugin checks active connection pool status for data sources and XA data sources. User can set warning and critical percentage as per requirement. It accepts 8 parameters in order to work properly and all eight parameters are mandatory.
> - --host| -H =  IP address of the host machine.
> - --port | -P = Port number of Jboss host
> - --user | -u = User name for Jboss management UI
> - --password | -p = Password for Jboss management console
> - --dstype | -t = Name of datasource type. There are only two types of data sources user can opt [e.g data-source or xa-data-source]
> - --dsname | -n = Name of data source, for example. ExampleDS
> - --warning | -w = Warning percentage, for example 50
> - --critical | -c = Critical percentage, for example 80

**Example**

    check_jboss_ds_count.py -H localhost -P 9990 -u gurvinder -p hell1wor1d! -t data-source -n ExampleDS -w 50 -c 80

**Output**

    INFO:Active Count=0, Available Count=20, Max Used Count=0| active_count=0, available_count=20, maxused_count=0
