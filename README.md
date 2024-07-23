# oom-query-engine-stats
comparing out of memory capability of a few different query engines

I use python 3.11 to run the experiment. the following command will install all required dependency.
```bash
pip install -r requirements.txt
```

There is only 3 files as for the 9gb test I only change the data being read in s3 through wildcard syntax. 

I got the following using t3.medium in aws

duckdb 9gb: 407.12 s 
polars 9gb:  129.14 s
chdb 9gb:  254.35 s

duckdb 18gb: Out of Memory Error
polars 18gb: 259.94 s
chdb 18gb: 580.001 s