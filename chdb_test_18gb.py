import os
import chdb
import time
from dotenv import load_dotenv

#load dotenv
load_dotenv()

#get environment variables
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')

#chdb can do this in one query instead
query = f"""
INSERT INTO FUNCTION
   s3(
       'https://oom-exp-results.s3.amazonaws.com/results_chdb_18gb.csv',
       '{S3_ACCESS_KEY}',
       '{S3_SECRET_KEY}',
       'CSV'
    )
SELECT date, sum(failure) as failures
FROM s3('https://duckdb-backblaze-data.s3.amazonaws.com/*.csv', '{S3_ACCESS_KEY}', '{S3_SECRET_KEY}')
GROUP BY date
SETTINGS s3_truncate_on_insert=1
"""

#end the timer
time_start = time.time()

#run oom query
chdb.query(query)

#end the timer
time_elapsed = time.time() - time_start

print(f"finished running oom query: {time_elapsed} seconds")
