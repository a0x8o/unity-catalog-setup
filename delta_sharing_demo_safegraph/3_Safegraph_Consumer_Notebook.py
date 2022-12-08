# Databricks notebook source
# DBTITLE 0,Let's Start With the Vast and Trusted Python Developers as Consumers
# MAGIC %md
# MAGIC ## Consuming Delta Shares
# MAGIC <b> On Databricks AND Anywhere Else Today <br>
# MAGIC `delta-sharing` is available as a python package on pypi. <br>
# MAGIC 
# MAGIC This simplifies the consumer side integration; anyone who can run python can consume shared data via SharingClient object. <br>
# MAGIC For this demo we have pre-installed delta-sharing on the cluster so that it available to all notebooks. 

# COMMAND ----------

import delta_sharing

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Simply Gain Access
# MAGIC <b> How do we gain access to the data once we install delta-sharing? <br>
# MAGIC 
# MAGIC Safegraph created a recipient entity for this demo, giving our team access to a Delta Share that is data sitting in their S3 bucket. This generated an activation link. <br>
# MAGIC That URL leads to a website for us to download a credential file that contains a long-term access token. <br>
# MAGIC Following the link will be take the recipient to an activation page that looks similar to this:
# MAGIC 
# MAGIC <img src="https://raw.githubusercontent.com/databricks/tech-talks/master/images/kanonymity_share_activation.png" width=600>
# MAGIC 
# MAGIC 
# MAGIC From this site the .share credential file can be downloaded by the recipient. This file contains the information and authorization token needed to access the Share. <br>
# MAGIC The contents of the file will look similar to the following example.
# MAGIC 
# MAGIC 
# MAGIC <img src="https://raw.githubusercontent.com/databricks/tech-talks/master/images/delta_sharing_cred_file_3.png" width="800">
# MAGIC 
# MAGIC **Due to the sensitive nature of the token, be sure to save it in a secure location.**

# COMMAND ----------

profile_file = '/dbfs/FileStore/sg_test_share.share'

# Create a SharingClient
client = delta_sharing.SharingClient(profile_file)

# List all shared tables.
client.list_all_tables()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pandas Query
# MAGIC #### Millions of Users Worldwide
# MAGIC 
# MAGIC <b> From Databricks and Anywhere Else Today <br>
# MAGIC 
# MAGIC Delta sharing allows us to access data via Pandas connector. <br>
# MAGIC To access the shared data we require a properly constructed url. <br>
# MAGIC The expected format of the url is: < profile_file \>#< share_id \>.< database \>.< table \><br>

# COMMAND ----------

# DBTITLE 0,Construct URL
places_table_url = f"{profile_file}#sg_test_share.safegraph.safegraph_core_places_test"
spend_table_url = f"{profile_file}#sg_test_share.safegraph.safegraph_spend"
core_places_df = delta_sharing.load_as_pandas(places_table_url)
spend_df = delta_sharing.load_as_pandas(spend_table_url)

# COMMAND ----------

# DBTITLE 1,Quickly Display Data
spend_df.head()

# COMMAND ----------

# DBTITLE 1,Unique Brands Provided
spend_df.groupby('brands').brands.nunique()

# COMMAND ----------

# DBTITLE 1,Explore Spend vs. Raw Customers for Circle K
import matplotlib.pyplot as plt

# Use delta sharing client to load data
spend_df.plot(x="raw_total_spend", y="raw_num_customers", kind="scatter",
        colormap="YlOrRd")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark Query
# MAGIC #### Sharing in Production
# MAGIC <b> From Databricks and Anywhere Else Today <br>
# MAGIC 
# MAGIC Similarly to Pandas connect delta sharing comes with a spark connector. <br>
# MAGIC The way to specify the location of profile file slightly differs between connectors. <br>
# MAGIC For spark connector the profile file path needs to be HDFS compliant. <br>

# COMMAND ----------

profile_file = '/FileStore/sg_test_share.share'
table_url = f"{profile_file}#sg_test_share.safegraph.safegraph_spend"
spark_df = delta_sharing.load_as_spark(table_url)
display(spark_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Databricks Spark SQL
# MAGIC <b> Best Practice for Setting up Delta Sharing on Databricks with a Credential File <br>
# MAGIC #### Our Security Best Practice Recommendation on Databricks: 
# MAGIC 1. Save this token in an S3 location that only an administrator can access. 
# MAGIC 2. Use a version of this notebook to access this token file and create the Delta Sharing Table in your metastore ONE TIME ONLY!
# MAGIC 3. _(Create a scheduled pipeline that copies the data fromt the share to a table in your cloud account)_
# MAGIC 4. Use normal process for access control (Table ACLs, etc) to control user access to the data

# COMMAND ----------

# DBTITLE 0,Create SQL Table using 'deltasharing' as a datasource
# MAGIC %sql
# MAGIC --We need to provide the url as: `< profile_file >#< share_id >.< database >.< table >` <br>
# MAGIC CREATE DATABASE IF NOT EXISTS safegraph_data;
# MAGIC USE safegraph_data;
# MAGIC DROP TABLE IF EXISTS safegraph_core_places_test;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS safegraph_core_places_test
# MAGIC     USING deltaSharing
# MAGIC     LOCATION "dbfs:/FileStore/sg_test_share.share#sg_test_share.safegraph.safegraph_core_places_test";
# MAGIC   CREATE TABLE IF NOT EXISTS safegraph_spend
# MAGIC     USING deltaSharing
# MAGIC     LOCATION "dbfs:/FileStore/sg_test_share.share#sg_test_share.safegraph.safegraph_spend"  

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM safegraph_core_places_test

# COMMAND ----------

# MAGIC %md 
# MAGIC # Power BI
# MAGIC <video width="320" height="240" controls>
# MAGIC   <source src="movie.mp4" type="video/mp4">
# MAGIC   <source src="movie.ogg" type="video/ogg">
# MAGIC Your browser does not support the video tag.
# MAGIC </video>

# COMMAND ----------

slide_id = '1Q-WtMS4O223GcehN-NH9nHedxozJEoQASyMpO0WtWr0'
slide_number = '1'

displayHTML(f'''

<iframe
  src="https://docs.google.com/presentation/d/{slide_id}/embed?slide={slide_number}&rm=minimal"
  frameborder="0"
  width="80%"
  height="700"
></iframe>

''')

# COMMAND ----------

# MAGIC %md
# MAGIC #Pycharm, Python IDE

# COMMAND ----------

slide_id = '1Q-WtMS4O223GcehN-NH9nHedxozJEoQASyMpO0WtWr0'
slide_number = '2'

displayHTML(f'''

<iframe
  src="https://docs.google.com/presentation/d/{slide_id}/embed?slide={slide_number}&rm=minimal"
  frameborder="0"
  width="80%"
  height="700"
></iframe>

''')

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC <b> [Safegraph Provider Demo]($./2_Safegraph_Provider_Notebook)   
# MAGIC <b> use cluster : demo_deltasharing_multi_language_single_user
