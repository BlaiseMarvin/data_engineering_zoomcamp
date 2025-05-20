from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .master("local")\
        .appName("test")\
        .getOrCreate()

data = [
    ('James','','Smith','1991-04-01','M',3000),
    ()
]