-- Databricks notebook source
-- DBTITLE 0,B2B Data Exchange with Delta Sharing
-- MAGIC %md
-- MAGIC 
-- MAGIC # Data Partner | [SafeGraph](https://www.safegraph.com/?utm_source=juntodemonotebook&utm_medium=referral&utm_campaign=junto_launch_demonotebook201911)<img src="https://i.ibb.co/vdNHFZN/deltasharingimage.png" width="55" height="60" />
-- MAGIC   
-- MAGIC To Illustrate let's us a real world example with a partner data provider already on <b>Delta Sharing</b>.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #Delta Sharing
-- MAGIC In Delta Sharing, it all starts with a Delta Lake table registered in the Delta Sharing Server by the data provider. This is where access permissions are established as to whom may receive the data.
-- MAGIC - Client authenticates to Sharing Server
-- MAGIC - Client requests a table (including filters)
-- MAGIC - Server checks access permissions
-- MAGIC - Server generates and returns pre-signed short-lived URLs
-- MAGIC - Client uses URLs to directly read files from object storage
-- MAGIC <br>
-- MAGIC <br>
-- MAGIC <img src="https://i.ibb.co/cXZf44Y/Screen-Shot-2022-03-11-at-1-50-57-PM.png" width="800">

-- COMMAND ----------

-- DBTITLE 0,Scenario 1: The Data Provider is a Databricks Customer
-- MAGIC %md
-- MAGIC ## Unity Catalog
-- MAGIC ##### Simple Administration with Unity Catalog as your entitlement layer Provided by Databricks
-- MAGIC 1. As a data provider, Unity Catalog will administer over delta shares and share data on Unity Catalog with other organizations
-- MAGIC 2. Unity Catalog’s security model is based on standard ANSI SQL, to grant permissions at the level of databases, tables, views, rows and columns </b> <br>
-- MAGIC 3. These organizations can then access the data using open source Apache Spark or pandas on any computing platform (including, but not limited to, Databricks). <br> <br>
-- MAGIC <img src="https://i.ibb.co/3YMznGv/Screen-Shot-2022-03-16-at-11-28-20-AM.png" width="800">
-- MAGIC                                                                                                 

-- COMMAND ----------

--CREATE WIDGET TEXT CatalogName DEFAULT "deltasharing";
--CREATE WIDGET TEXT ShareName DEFAULT "sg_test_share";
--CREATE WIDGET TEXT  RecipientName DEFAULT "safegraph_demo"

-- COMMAND ----------

-- DBTITLE 1,Run Cell Prior to Demo Execution
-- RUN THIS CELL PRIOR TO DEMO For Re-Execution 
-- make sure you are using a delta sharing enabled workspace & a UC enabled Cluster
DROP RECIPIENT IF EXISTS $RecipientName;
DROP SHARE IF EXISTS $ShareName;

-- COMMAND ----------

-- DBTITLE 1,Use Catalog Already Created for External Data to Share
USE CATALOG $CatalogName

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #1: Create Share
-- MAGIC - Create share under Unity Catalog in Standard ANSI SQL (CLI/API capabilities not demoed but fully supported)

-- COMMAND ----------

CREATE SHARE IF NOT EXISTS $ShareName COMMENT 'Test Data to Display Safegraphs Delta Sharing Distribution Mechanism';

-- COMMAND ----------

-- DBTITLE 1,View Share
DESCRIBE SHARE $ShareName;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #2. Add Full Tables

-- COMMAND ----------

ALTER SHARE $ShareName ADD TABLE deltasharing.safegraph.safegraph_core_places_test;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 3. Add Partial Tables
-- MAGIC <b> Filter to Only Share a Portion of the Flights Table Using "=" & LIKE Operators. </b> </br>
-- MAGIC <b> Then Leverage Customizable Table Display Names for an Nice Consumer Searching Experience </b> </br>
-- MAGIC <br>
-- MAGIC Specifying partition specification when adding a table to a Share allows you to share table’s data by its pre-defined partitions. Below is an example of sharing partial data in the `spend` table: 1) all data filtered to a specific date range, 2) all data for 2021 using the LIKE operator in one

-- COMMAND ----------

-- DBTITLE 0,Step 3: Add Full & Partial Tables to Share Partition 
ALTER SHARE $ShareName ADD TABLE deltasharing.safegraph.safegraph_spend PARTITION (date_range LIKE "2021-03%") as safegraph.`safegraph_spend`;

-- COMMAND ----------

-- DBTITLE 1,View Tables in Share
SHOW ALL IN SHARE $ShareName;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 4. Create Recipient(s)

-- COMMAND ----------

-- DBTITLE 0,Step 6: Create a Recipient(s)
CREATE RECIPIENT $RecipientName;

-- COMMAND ----------

-- DBTITLE 1,Show Recipient
DESCRIBE RECIPIENT $RecipientName;

-- COMMAND ----------

-- DBTITLE 0,Download Share Profile & Store on DBFS - PURELY FOR DEMO
-- MAGIC %python
-- MAGIC import urllib.request
-- MAGIC share = getArgument("ShareName")
-- MAGIC recipient = getArgument("RecipientName")
-- MAGIC sql(""" DROP RECIPIENT IF EXISTS {} """.format(recipient))
-- MAGIC df = sql(""" CREATE RECIPIENT {} """.format(recipient))
-- MAGIC share = getArgument("ShareName")
-- MAGIC recipient = getArgument("RecipientName")
-- MAGIC link = df.collect()[0][4].replace('delta_sharing/retrieve_config.html?','api/2.0/unity-catalog/public/data_sharing_activation/')
-- MAGIC urllib.request.urlretrieve(link, "/tmp/" + share + ".share")
-- MAGIC dbutils.fs.mv("file:/tmp/" + share + ".share", "dbfs:/FileStore/" + share + ".share")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 5. Grant Access 
-- MAGIC <br>
-- MAGIC --'SELECT' gives read only permissions on all tables in the share

-- COMMAND ----------

-- DBTITLE 0,Step 8: Define which Data to Share, and Level of Access 
GRANT SELECT ON SHARE $ShareName TO RECIPIENT $RecipientName;

-- COMMAND ----------

-- DBTITLE 1,Verify Level of Access
SHOW GRANT ON SHARE $ShareName;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 5. Share with Customer <br>
-- MAGIC Activation link can be shared with recipient <br>
-- MAGIC <img src="https://raw.githubusercontent.com/databricks/tech-talks/master/images/kanonymity_share_activation.png" width=600>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # 6. Revoke Access
-- MAGIC - If needed you can revoke access at anytime with the same simple SQL statement below <br>
-- MAGIC `REVOKE SELECT ON SHARE safegraph_demo FROM RECIPIENT safegraph_demo`

-- COMMAND ----------

-- DBTITLE 1,View Shares
SHOW ALL IN SHARE $ShareName;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC <b> [Safegraph Consumer Demo]($./3_Safegraph_Consumer_Notebook) <br>
-- MAGIC <b>use cluster: demo_deltasharing_reciever
