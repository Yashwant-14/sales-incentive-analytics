import shutil
import datetime
from resources.dev import config
from src.main.utility.encrypt_decrypt import *
from src.main.utility.s3_client_object import S3ClientProvider
from src.main.utility.logging_config import logger
import os
from src.main.utility.my_sql_session import *
from src.main.read.aws_read import *
from src.main.download.aws_file_download import *
from src.main.utility.spark_session import *
from src.main.move.move_files import *
from src.main.read.database_read import *
from src.main.transformations.jobs.dimension_tables_join import *
from src.main.transformations.jobs.customer_mart_sql_transform_write import *
from src.main.transformations.jobs.sales_mart_sql_transformation_write import *
from src.main.write.parquet_writer import *
from src.main.upload.upload_to_s3 import *
from src.main.delete.local_file_delete import *





# ***********************************S3 connection using Boto3****************************************

aws_access_key = config.aws_access_key # encrypted access_key
aws_secret_key = config.aws_secret_key # encrypted sectet_key

s3_client_provider = S3ClientProvider(decrypt(aws_access_key), decrypt(aws_secret_key))
s3_client = s3_client_provider.get_client()

response = s3_client.list_buckets()
print(response['Buckets'])
#logger.info("List of S3 buckets: %s", response['Buckets'])


# ***********************************Connecting Sql with Python using mySQL connector***********************************

# check if local directory has already a file
# if file is there then check id the same file is present in the staging area
# with status as A. If so then don't delete and try to re-run
# Else give an error and not process the next file
# os.listdir() -> prints all files 

print(os.listdir(config.local_directory))
csv_files = [file for file in os.listdir(config.local_directory) if file.endswith('.csv')]
#csv_files contains all the files names that ends with '.csv' in that folder
connection= get_mysql_connection()
cursor = connection.cursor()

total_csv_files=[]

if csv_files:
    for file in csv_files:
        total_csv_files.append(file)
    
    statement = f'''
                    select distinct file_name
                    from {config.database_name}.product_staging_table 
                    where file_name in ({str(total_csv_files)[1:-1]}) and status='I'

                '''
    logger.info(f"dynamically statement created: {statement}")
    cursor.execute(statement)
    data= cursor.fetchall()
    if data:
        logger.info("Your last run was failed please check")
    else:
        logger.info("NO Record Match")
else:
    logger.info("Last run was successful O!!O")


# ************************************Downloading files from S3************************************************

try:
    s3_reader=S3Reader()
    #Bucket name should come from table
    folder_path=config.sales_data
    s3_absolute_file_path=s3_reader.list_files(s3_client,config.bucket_name,folder_path=folder_path)
    # s3_absolute_file_path will return a list of file path
    logger.info(f"Absolute path on S3 bucket for CSV file {s3_absolute_file_path} ")
    if not s3_absolute_file_path:
        logger.info(f"No files abailable at {folder_path}")
        raise Exception("No Data available to process")
except Exception as e:
    logger.info("Exited with error:- %s",e)
   


bucket_name= config.bucket_name
local_directory= config.local_directory

prefix= f"s3://{bucket_name}/"
file_path =[url[len(prefix):] for url in s3_absolute_file_path]
logging.info("File path available on s3 under %s bucket and folder name is %s" , bucket_name,file_path)
try:
    downloader = S3FileDownloader(s3_client,bucket_name,local_directory)
    downloader.download_files(file_path)
except Exception as e:
    logger.info("File download error: %s",e)
    sys.exit()
# Get a list of all files in the local directory


all_files= os.listdir(local_directory)
logger.info(f"List of files present at my local directory after download {all_files}")

#Filter files with ".csv" in their name and create absolute paths

if all_files:
    csv_files=[]
    error_files=[]
    for files in all_files:
        if files.endswith(".csv"):
            csv_files.append(os.path .abspath(os.path.join(local_directory,files)))
        else:
            error_files.append(os.path .abspath(os.path.join(local_directory,files)))
    if not csv_files:
        logger.error("No CSV data available to process the request")
        raise Exception("No CSV data available to process the request")
else:
    logger.error("There is no data to process.")



# ***********************************Make csv lines convert into a list of comma sepearated***********************************


logger.info("***********************************Listing the files***********************************")
logger.info(f"List of csv files that needs to be processed {csv_files}")

logger.info("***********************************Creating spark session***********************************")

spark=spark_session()

logger.info("***********************************Spark Session Created***********************************")

# check the required column in the schema of csv files 
# if not required columns keep it in a list or error_files 
# else union all the data into one dataframe

logger.info("***********************************Checking schema for data loaded in s3***********************************")

correct_files=[]
for file_path in csv_files:
    data_schema= spark.read.format("csv")\
                            .option("header","true")\
                            .load(file_path).columns
    logger.info(f"Schema for the {file_path} is {data_schema}")
    logger.info(f"Mandatory columns schema is {config.mandatory_columns}")
    missing_columns=set(config.mandatory_columns)-set(data_schema)
    logger.info(f"Missing Columns are {missing_columns}")

    if missing_columns:
        error_files.append(file_path)
    else:
        logger.info(f"No missing column for the {file_path}")
        correct_files.append(file_path)

logger.info(f"***********************************List of correct files***********************************{correct_files}")
logger.info(f"***********************************List of error files***********************************{error_files}")
logger.info(f"***********************************Moving Error data to error directory if any***********************************")

# Move the data to Error directory on local  

if error_files:
    for file_path in error_files:
        if os.path.exists(file_path):

            file_name= os.path.basename(file_path)
            destination_path=os.path.join(config.error_folder_path_local,file_name)

            shutil.move(file_path,destination_path)
            logger.info(f"Moved '{file_name}' form s3 file path to '{destination_path}'")

            source_prefix= config.sales_data
            destination_prefix= config.s3_error_directory

            message = move_s3_to_s3(s3_client, config.bucket_name,source_prefix,destination_prefix)
            logger.info(f"{message}")
        else:
            logger.error(f"'{file_path}' does not exist.")
else:
    logger.info("***********************************There is no error files available at our dataset***********************************")



# Additional columns needs to be take care of
#Determine extra columns
# Before running the process
#stage table needs to be updated with status as Active(A) or inactive(I)

logger.info(f"***********************************Updating the product_staging_table that we have started the process***********************************")
insert_statements=[]
db_name=config.database_name
current_date= datetime.datetime.now()
formatted_date= current_date.strftime("%Y-%m-%d %H:%M:%S")
if correct_files:
    for file in correct_files:
       
        if os.path.exists(file):
            filename= os.path.basename(file)
            statements=f'''insert into {db_name}.{config.product_staging_table}
                            (file_name,file_location,created_date, status)
                            values('{filename}','{filename}','{formatted_date}','A')'''
            insert_statements.append(statements)
    logger.info(f"Insert statement created for staging table --- {insert_statements}")
    logger.info(f"***********************************Connecting with MYSQL server***********************************")
    connection = get_mysql_connection()
    cursor=connection.cursor()
    logger.info("***********************************MY SQL server Connected successfully***********************************")

    for statement in insert_statements:
        cursor.execute(statement)
        connection.commit()
    cursor.close()
    connection.close()
else:
    logger.error("***********************************There is no files to process***********************************")
    raise Exception("***********************************NO Data available with correct files***********************************")




logger.info("***********************************Staging table updated Successfully***********************************")
logger.info("***********************************Fixing extra Columns comming form source***********************************")

schema= StructType([
    StructField("customer_id", IntegerType(),True),
    StructField("store_id", IntegerType(),True),
    StructField("product_name", StringType(),True),
    StructField("sales_date", DateType(),True),
    StructField("sales_person_id", IntegerType(),True),
    StructField("price", FloatType(),True),
    StructField("quantity", IntegerType(),True),
    StructField("total_cost", FloatType(),True),
    StructField("additional_column", StringType(),True),
])

final_df_to_process= spark.createDataFrame([],schema=schema)
#Creating a new column with concatenated values of extra columns

for data in correct_files:
    data_df=spark.read.format("csv")\
                        .option("header","true")\
                        .option("inferSchema","true")\
                        .load(data)
    
    data_schema=data_df.columns 
    extra_columns= list(set(data_schema)-set(config.mandatory_columns))
    logger.info(f"Extra columns present at source is {extra_columns}")

    if extra_columns:
        data_df=data_df.withColumn("additional_column",concat_ws(",",*extra_columns))\
                        .select("customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost","additional_column")
        logger.info(f"processed {data} and added 'additional_column'")
    else:
        data_df=data_df.withColumn("additional_column",lit(None))\
                        .select("customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost","additional_column")
        
    final_df_to_process= final_df_to_process.union(data_df)

logger.info("***********************************Final Dataframe from source which will be going to***********************************")
final_df_to_process.show() #This is the fact table after all the error checks


# Enrich te data from all dimension table
# also create a datamart for sales_team and their incentive,address and all
# another datamart for customer who bought how much each days of month
# for every month there should be a file and inside that there should be a store_id segrigation
# Read the data from parquet and generate a csv file
# in which there will be a sales_person_name,sales_person_store_id,sales_person_total_billing_done_for_each_month, total_incentive


# Connecting with DatabaseReader
database_client= DatabaseReader(config.url,config.properties)

# Creating df for all tables
# customer table
logger.info("***********************************Loading Customer table into customer_table_df***********************************")
customer_table_df= database_client.create_dataframe(spark,config.customer_table_name)
# customer_table_df.show()

# product table
logger.info("***********************************Loading product table into product_table_df***********************************")
product_table_df= database_client.create_dataframe(spark,config.product_table)


# product_staging_table 
logger.info("***********************************Loading product_staging_table into product_staging_table_df***********************************")
product_staging_table_df= database_client.create_dataframe(spark,config.product_staging_table)
# product_staging_table_df.show()

# sales_team_table
logger.info("***********************************Loading sales_team_table into sales_team_table***********************************")
sales_team_table_df= database_client.create_dataframe(spark,config.sales_team_table)
# sales_team_table_df.show()

# store_table
logger.info("***********************************Loading Store table into store_table***********************************")
store_table_df= database_client.create_dataframe(spark,config.store_table )
# store_table_df.show()


# After joining all the dimension table with fact table s3_customer_store_sales_df_join is the df with all values 
s3_customer_store_sales_df_join= dimensions_table_join(final_df_to_process,customer_table_df,store_table_df,sales_team_table_df)

#Final enriched data
logger.info("***********************************Final Enriched Data***********************************")
s3_customer_store_sales_df_join.show()


# Write teh customer data into customer data mart in parquet format
# file will be written to local first 
# Move the RAW data to s3 bucket for reporting tool
# Write reporting data into MYSQL table also

logger.info("***********************************Write the data into Customer Data Mart***********************************")

final_customer_data_mart_df=s3_customer_store_sales_df_join\
                            .select('customer_id','first_name','customer_address','pincode','phone_number','sales_date','total_cost')

logger.info("***********************************Final Data for Customer Data Mart***********************************")
final_customer_data_mart_df.show()

parquet_writer = ParquetWriter('overwrite','parquet')
parquet_writer.dataframe_writer(final_customer_data_mart_df,config.customer_data_mart_local_file)

logger.info(f"***********************************Customer data written to local disk at{config.customer_data_mart_local_file}***********************************")

# Move data on s3 bucket for customer_data_mart

logger.info("***********************************Data Movement from local to s3 for customer data mart***********************************")
s3_uploader= UploadToS3(s3_client)
s3_directory=config.s3_customer_datamart_directory
message=s3_uploader.upload_to_s3(s3_directory,config.bucket_name,config.customer_data_mart_local_file)
logger.info(f"{message}")


#sales Data mart
logger.info("***********************************Write the data into Sales Data Mart***********************************")
final_sales_team_data_mart_df=s3_customer_store_sales_df_join\
                                .select("store_id","sales_person_id","sales_person_first_name","sales_person_last_name","store_manager_name",
                                        "manager_id","is_manager","sales_person_address","sales_person_pincode","sales_date","total_cost",
                                        expr("SUBSTRING(sales_date,1,7)as sales_month"))
final_sales_team_data_mart_df.show()
parquet_writer.dataframe_writer(final_sales_team_data_mart_df,config.sales_team_data_mart_local_file)
logger.info(f"***********************************Customer data written to local disk at{config.sales_team_data_mart_local_file}*******************")

#Move data on s3 bucket for sales team data_mart

logger.info("***********************************Data Movement from local to s3 Sales team data mart***********************************")
s3_uploader= UploadToS3(s3_client)
s3_directory=config.s3_sales_datamart_directory
message=s3_uploader.upload_to_s3(s3_directory,config.bucket_name,config.sales_team_data_mart_local_file)
logger.info(f"{message}")

# Also writing the data into partitions

final_sales_team_data_mart_df.write.format("parquet")\
                                    .option("header","true")\
                                    .mode("overwrite")\
                                    .partitionBy("sales_month","store_id")\
                                    .option("path",config.sales_team_data_mart_partitioned_local_file)\
                                    .save()

logger.info("**************sales_team_data_mart partitioned by sales_month and store_id in local ***********************************")

# Move data on s3 for partitioned folder
s3_prefix=f"{config.s3_sales_partitioned_data_mart}"
current_epoch= int(datetime.datetime.now().timestamp())*1000
for root,dir,files in os.walk(config.sales_team_data_mart_partitioned_local_file):
    for file in files:
        print(file)
        local_file_path=os.path.join(root,file)
        relative_file_path=os.path.relpath(local_file_path,config.sales_team_data_mart_partitioned_local_file)
        s3_key=f"{s3_prefix}/{current_epoch}/{relative_file_path}"
        s3_client.upload_file(local_file_path,config.bucket_name,s3_key)


#calculateion for customer data mart
#find out the customer total purchase every month
#write the data into MYSQL table


logger.info("***********************************Calculating customer every month purchased amount***********************************")
customer_mart_calculation_table_write(final_customer_data_mart_df)
logger.info("***********************************Calculation of customer mart done and written into the table***********************************")

# calculation for sales team mart
# find out the total sales done by each sales person every month
# give the top 1% incentive of total sales of the month
#Rest sales Person will get nothing 
# write the data into MySQL table

logger.info("************Calculating sales every month billed amount*************************")
sales_mart_calculation_table_write(final_sales_team_data_mart_df)
logger.info("************Calculation of sales mart done and written into the table*************************")


####################################   Last Step   ###########################

#Move the file on s3 into processed folder and delete the local files

source_prefix=config.sales_data
destination_prefix=config.s3_processed_directory
message=move_s3_to_s3(s3_client,config.bucket_name,source_prefix,destination_prefix)
logger.info(f"{message}")


logger.info("***********************************Deleting sales data from local ********************************")
delete_local_file(config.local_directory)
logger.info("***********************************Deleted the sales data from local******************************")

logger.info("***********************************Deleting Customer data from local *****************************")
delete_local_file(config.customer_data_mart_local_file)
logger.info("***********************************Deleted the customer data from local***************************")


logger.info("***********************************Deleting sales team data from local ***************************")
delete_local_file(config.sales_team_data_mart_local_file)
logger.info("***********************************Deleted the sales team data from local*************************")


logger.info("***********************************Deleting sales partition data from local ***********************")
delete_local_file(config.sales_team_data_mart_partitioned_local_file)
logger.info("***********************************Deleted the sales partition data from local*********************")

# update the status of staging table 

update_statement=[]
if correct_files:
    for file in correct_files:
        filename= os.path.basename(file)
        statements= f''' UPDATE {db_name}.{config.product_staging_table}
                            set status='I',updated_date='{formatted_date}'
                            where file_name="{file_name}"'''
        
        update_statement.append(statements)
    logger.info(f"Updated statement created for staging table --- {update_statement}")
    logger.info("*********************Connecting with MY SQL server ********************************")
    connection=get_mysql_connection()
    cursor=connection.cursor()
    logger.info("********************** MY SQL server connected successfully ******************************")

    for statement in update_statement:
        cursor.execute(statement)
        connection.commit()
    cursor.close()
    connection.close()

else:
    logger.error("************************There is some error in process in between****************************")
    sys.exit()

input("Press enter to terminate")

