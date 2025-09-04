from pyspark.sql.functions import *
from src.main.utility.logging_config import *
#enriching the data from different table
def dimensions_table_join(final_df_to_process,
                         customer_table_df,store_table_df,sales_team_table_df):

    #step 1 where i am adding customer table
    # final_df_to_process.alias("s3_data") \
    #     .join(customer_table_df.alias("ct"),
    #           col("s3_data.customer_id") == col("ct.customer_id"),"inner") \
    #     .show()

    #But i do not need all the columns so dropping it
    #save the result into s3_customer_df_join
    logger.info("Joining the final_df_to_process with customer_table_df ")
    s3_customer_df_join = final_df_to_process.alias("s3_data") \
        .join(customer_table_df.alias("ct"),
              col("s3_data.customer_id") == col("ct.customer_id"),"inner") \
        .select(col('s3_data.customer_id'),'store_id','sales_date','sales_person_id','total_cost','first_name','last_name',col('address').alias("customer_address"),'pincode','phone_number')\
        .orderBy("customer_id")
      #   .drop("product_name","price","quantity","additional_column",
      #         "customer_id","customer_joining_date")

#     s3_customer_df_join.show()

    #step 2 where i am adding store table details
    # s3_customer_df_join.join(store_table_df,
    #                          store_table_df["id"]==s3_customer_df_join["store_id"],
    #                          "inner").show()

    #But i do not need all the columns so dropping it
    #save the result into s3_customer_store_df_join
    logger.info("Joining the s3_customer_df_join with store_table_df ")

    s3_customer_store_df_join= s3_customer_df_join.join(store_table_df,
                             store_table_df["id"]==s3_customer_df_join["store_id"],
                             "inner")\
                        .drop("id","store_pincode","store_opening_date","reviews")

      
#     s3_customer_store_df_join.show()
    #step 3 where i am adding sales team table details
    # s3_customer_store_df_join.join(sales_team_table_df,
    #                          sales_team_table_df["id"]==s3_customer_store_df_join["sales_person_id"],
    #                          "inner").show()


    #But i do not need all the columns so dropping it
    #save the result into s3_customer_store_sales_df_join
    logger.info("Joining the s3_customer_store_df_join with sales_team_table_df ")


    s3_customer_store_sales_df_join = (
      s3_customer_store_df_join
      .join(sales_team_table_df.alias("st"),
            col("st.id") == s3_customer_store_df_join["sales_person_id"],
            "inner")
      .select(
            s3_customer_store_df_join["*"],   # keep all customer-store columns
            col("st.first_name").alias("sales_person_first_name"),
            col("st.last_name").alias("sales_person_last_name"),
            col("st.address").alias("sales_person_address"),
            col("st.pincode").alias("sales_person_pincode"),
            "st.manager_id","st.is_manager"
      )
      )
#     s3_customer_store_sales_df_join.show()

    return s3_customer_store_sales_df_join

