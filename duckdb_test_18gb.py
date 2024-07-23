import os
import duckdb
import time
from dotenv import load_dotenv

load_dotenv()

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')


qe_oom = duckdb.connect("persist_db.db")
qe_oom.sql(f"""
CREATE SECRET secret1 (
    TYPE S3,
    KEY_ID '{S3_ACCESS_KEY}',
    SECRET '{S3_SECRET_KEY}',
    REGION 'us-east-1'
)
""")

query = """
CREATE OR REPLACE VIEW metrics AS (
SELECT date, sum(failure) as failures
FROM read_csv_auto("s3://duckdb-backblaze-data/*.csv", ignore_errors = true, union_by_name = true)
GROUP BY date
)
"""

query_metrics = """
COPY metrics to 's3://oom-exp-results/results_duckdb_18gb.csv'
"""

time_start = time.time()

qe_oom.execute(query)
qe_oom.execute(query_metrics)

time_elapsed = time.time() - time_start

print(f"finished running oom query: {time_elapsed} seconds")
