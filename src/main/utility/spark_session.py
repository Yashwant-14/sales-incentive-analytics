import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from src.main.utility.logging_config import *

def spark_session():
    spark = SparkSession.builder.master("local[*]") \
        .appName("SIA")\
        .config("spark.driver.extraClassPath", "C:\\my_sql_spark_connector\\mysql-connector-j-9.4.0.jar") \
        .config("spark.hadoop.hadoop.native.lib", "false") \
        .getOrCreate()
    logger.info("spark session %s",spark)
    print(spark.sparkContext._jvm.org.apache.hadoop.util.VersionInfo.getVersion())

    return spark