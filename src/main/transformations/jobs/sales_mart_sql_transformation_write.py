from pyspark.sql.functions import *
from pyspark.sql.window import Window
from resources.dev import config
from src.main.write.database_write import DatabaseWriter
#calculation for sales_team mart
#find out the sales_person total billing amount every month
#write the data into sql table
def sales_mart_calculation_table_write(final_sales_team_data_mart_df):
    # Aggregate sales by store, salesperson, and month
    final_sales_team_data_mart = final_sales_team_data_mart_df \
        .withColumn("sales_month", substring(col("sales_date"), 1, 7)) \
        .groupBy("store_id", "sales_person_id", "sales_person_first_name", "sales_person_last_name", "sales_month") \
        .agg(sum("total_cost").alias("total_sales_every_month")) \
        .withColumn("full_name", concat(col("sales_person_first_name"), lit(" "), col("sales_person_last_name")))

    # Ranking within each store & month
    rank_window = Window.partitionBy("store_id", "sales_month").orderBy(col("total_sales_every_month").desc())

    final_sales_team_data_mart_table = final_sales_team_data_mart \
        .withColumn("rnk", rank().over(rank_window)) \
        .withColumn("incentive", when(col("rnk") == 1, col("total_sales_every_month") * 0.01).otherwise(lit(0))) \
        .withColumn("incentive", round(col("incentive"), 2)) \
        .withColumn("total_sales", col("total_sales_every_month")) \
        .select("store_id", "sales_person_id", "full_name", "sales_month", "total_sales", "incentive")

    # Write the data into MySQL sales_team table
    print("Writing the data into sales_team data mart")
    db_writer = DatabaseWriter(config.url, config.properties)
    db_writer.write_dataframe(final_sales_team_data_mart_table, config.sales_team_data_mart_table)
