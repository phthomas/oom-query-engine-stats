import s3fs
import os
import fnmatch
import polars as pl
import pyarrow.dataset as ds
import time
from dotenv import load_dotenv

#load dotenv
load_dotenv()

#get environment variables
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')

#set credentials for polars
storage_options = {
    "aws_access_key_id": f"{S3_ACCESS_KEY}",
    "aws_secret_access_key": f"{S3_SECRET_KEY}"
}

#set up s3 connection
s3_endpoint = f"s3://duckdb-backblaze-data"
fs = s3fs.S3FileSystem(key=f"{S3_ACCESS_KEY}", secret=f"{S3_SECRET_KEY}")

#filter data to read
file_to_read = fnmatch.filter(fs.ls(s3_endpoint),"duckdb-backblaze-data/*.csv")

#create arrow tabular dataset --> polars has issues in lazily scanning csv
ds_to_read = ds.dataset(file_to_read, filesystem=fs, format='csv')

#lazy query
df = pl.scan_pyarrow_dataset(ds_to_read)
df = df.select(pl.col("date", "failure")).group_by("date").agg(
    failures = pl.sum("failure")
)

#start the timer
time_start = time.time()

#run query and write
with fs.open("s3://oom-exp-results/results_polars_18gb.csv", mode='wb') as f:
    df.collect().write_csv(f)

#end the timer
time_elapsed = time.time() - time_start

print(f"finished running oom query: {time_elapsed} seconds")
