import pandas as pd

# Define file paths
input_csv_file = 'cleaned_data.csv'  # Replace with your large CSV file path
output_csv_file = 'small_dataset.csv'  # Replace with your desired output CSV file path

# Define the range of rows to extract
start_row = 1467778  # Zero-based index
end_row = 1476790  # Zero-based index

# Use a more efficient approach to handle large datasets
# Read the CSV file with chunks and extract the specified rows
chunk_size = 100000  # Adjust based on your memory capacity
extracted_rows = []

for chunk in pd.read_csv(input_csv_file, chunksize=chunk_size):
    # Check if the chunk contains the desired row range
    chunk_start_row = max(start_row, chunk.index[0])
    chunk_end_row = min(end_row, chunk.index[-1] + 1)
    
    if chunk_end_row > chunk_start_row:
        # Extract rows within the current chunk
        extracted_chunk = chunk.iloc[chunk_start_row - chunk.index[0]:chunk_end_row - chunk.index[0]]
        extracted_rows.append(extracted_chunk)

# Concatenate all extracted rows into a single DataFrame
small_df = pd.concat(extracted_rows)

# Save the DataFrame to a new CSV file
small_df.to_csv(output_csv_file, index=False)

print(f"Extracted rows saved to {output_csv_file}")
