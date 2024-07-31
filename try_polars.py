import polars as pl
import csv

file_path = 'index.json'

count = 0

# Define the chunk size (number of lines to read at a time)
chunk_size = 100  # Adjust based on your memory capacity

# Open the file and process in chunks
with open(file_path, 'r') as f:
    reader = csv.DictReader(f)
    # Process each chunk
    while True:
        chunk_data = []
        try:
            # Read the next chunk of data
            for _ in range(chunk_size):
                chunk_data.append(next(reader))
        except StopIteration:
            # End of file reached
            pass
        
        if not chunk_data:
            # No more data to process
            break
        
        # Create a Polars DataFrame from the chunk
        df_chunk = pl.DataFrame(chunk_data)
        
        # Filter rows where Location is "us-east-1" and count them
        count += df_chunk.filter(pl.col('Location') == 'us-east-1').shape[0]

print(f'Number of rows with Location "us-east-1": {count}')
