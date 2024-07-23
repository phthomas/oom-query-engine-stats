# oom-query-engine-stats
comparing out of memory capability of a few different query engines

I use python 3.11 to run the experiment. the following command will install all required dependency.
```bash
foo@bar:~$ pip install -r requirements.txt
```

There is only 3 files as for the 9gb test I only change the data being read in s3 through wildcard syntax. 