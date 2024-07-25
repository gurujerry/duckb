# duckb
Playing with Duckdb

```bash
# Grab a big json file
wget https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json
# how big is it?
ls -alh index.json
#5.6G or 6,003,967,653
wc -l index.json 
#158,204,582 index.json
# Too big to save in github, so add to .gitignore
echo "index.json" >> .gitignore
# Grab duckdb
wget https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
rm -f *.zip
# Try convert to parquet https://github.com/duckdb/duckdb/discussions/6478
mkdir ./tmp
# So we don't OOB, we try to use temp files. Below tries currently faii
time echo "PRAGMA temp_directory='/tmp/';
            SET preserve_insertion_order=false;
            COPY (SELECT *
                 FROM read_json_objects('index.json'))
            TO 'duckdb.pq' (FORMAT 'PARQUET',
                            CODEC  'Snappy',
                            ROW_GROUP_SIZE 130099920,
                            PER_THREAD_OUTPUT TRUE);" \
    | ./duckdb
time echo "SET preserve_insertion_order=false;
           COPY (SELECT *
           FROM read_json_objects('index.json'))
           TO 'duckdb.pq' (FORMAT 'PARQUET',
                           CODEC  'Snappy');" \
    | ./duckdb
#Invalid Input Error: Expected top-level JSON array with format='array', but first character is '{' in file "index.json".
# Try setting format='auto' or format='newline_delimited'
# Random try, error: "Invalid Input Error: "maximum_object_size" of 16777216 bytes exceeded while reading file "index.json" (>33554428 bytes). Try increasing "maximum_object_size"."
./duckdb -c "PRAGMA temp_directory='/tmp/'; SELECT * FROM 'index.json'"

./duckdb -c "PRAGMA temp_directory='/tmp/';
            SET preserve_insertion_order=false;
            COPY (SELECT *
                 FROM read_json_objects('index.json')  (AUTO_DETECT true))
            TO 'duckdb.pq' (FORMAT 'PARQUET',
                            CODEC  'Snappy',
                            ROW_GROUP_SIZE 130099920,
                            PER_THREAD_OUTPUT TRUE);"

#./duckdb -c "PRAGMA temp_directory='/tmp/'; SELECT count(*) FROM 'index.json'"
# Try entering duckdb CLI and running oommands
./duckdb
SET preserve_insertion_order=false;
SET memory_limit='4GB';
#SET memory_limit='200MB';
SET temp_directory='./tmp/';
SET threads=2;
SELECT * FROM duckdb_settings();
"SELECT count(*) FROM 'index.json'"
<ctrl> + d
rm -rf *.pq
```

At this point, it's being a real PITA to try and use duckdb so let's see if we can use python to convert the `index.json` to parquet format at check the size difference.
Start by installing some libraries
```bash
pip install pandas pyarrow ijson
```

Try to Read and process the JSON file in chunks using ijson and Convert each chunk to a DataFrame and append it to a Parquet file in file [ijson_to_parquet.py](./ijson_to_parquet.py).

Just to see what removing preceding whitespace would make the json size look like, we can run:
[](./remove_whitespace.py)
```bash
python remove_whitespace.py
ls -al compressed_output.json
# 4.1G 326807926
```
