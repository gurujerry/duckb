import ijson
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Function to process and convert JSON chunks to Parquet
def convert_json_to_parquet(json_file_path, parquet_file_path, chunk_size=1000):
    # Open the JSON file
    with open(json_file_path, 'r') as file:
        # Initialize an empty list to hold JSON objects
        rows = []
        # Use ijson to parse the JSON file incrementally
        objects = ijson.items(file, 'item')  # Adjust 'item' to match the top-level structure of your JSON
        
        # Initialize a counter
        count = 0

        # Process each JSON object
        for obj in objects:
            rows.append(obj)
            count += 1
            
            # If we reach the chunk size, convert the chunk to a DataFrame and write to Parquet
            if count % chunk_size == 0:
                df = pd.DataFrame(rows)
                table = pa.Table.from_pandas(df)
                
                # Append to the Parquet file
                if count == chunk_size:
                    pq.write_table(table, parquet_file_path)
                else:
                    pq.write_table(table, parquet_file_path, append=True)
                
                # Clear the list for the next chunk
                rows.clear()

        # Process any remaining rows
        if rows:
            df = pd.DataFrame(rows)
            table = pa.Table.from_pandas(df)
            pq.write_table(table, parquet_file_path, append=True)

# Paths to your input JSON file and output Parquet file
json_file_path = 'index.json'
parquet_file_path = 'output_file.parquet'

# Convert the JSON file to Parquet in chunks
convert_json_to_parquet(json_file_path, parquet_file_path)
