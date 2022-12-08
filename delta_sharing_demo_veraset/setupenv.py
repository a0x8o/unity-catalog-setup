# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dveraset_movements
# MAGIC     USING deltaSharing
# MAGIC     LOCATION "dbfs:/FileStore/veraset.share#veraset_databricks_share.mill_db.movement_panel"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS veraset comment "Veraset Provided Data for Databricks Demonstrations"

# COMMAND ----------

# MAGIC %sql 
# MAGIC USE CATALOG deltasharing

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG deltasharing;
# MAGIC USE SCHEMA veraset;
# MAGIC CREATE OR REPLACE TABLE movements USING DELTA AS
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   hive_metastore.default.veraset_movements;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE veraset.movements

# COMMAND ----------

import delta_sharing

# COMMAND ----------

profile_file = '/dbfs/FileStore/veraset.share'

# Create a SharingClient
client = delta_sharing.SharingClient(profile_file)

# List all shared tables.
client.list_all_tables()

# COMMAND ----------


