import pandas as pd
import os

# Initialize an empty DataFrame to store results
df_result = pd.DataFrame()

# Specify the folder to search
base_folder = 'news'

# Walk through all files in the directory (including subdirectories)
for root, _, files in os.walk(base_folder):
    for file in files:
        if file.endswith('.csv'):  # Process only CSV files
            file_path = os.path.join(root, file)
            try:
                # Read the CSV file, assuming tab-separated
                df = pd.read_csv(file_path, sep='\t')
                # Concatenate the cleaned DataFrame to the result
                df_result = pd.concat([df_result, df], ignore_index=True)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Drop rows with missing 'content' and remove duplicates based on 'link'
df_result = df_result.dropna(subset=['content'])
df_result = df_result.drop_duplicates(subset=['link'])
df_result = df_result.drop_duplicates(subset=['title'])
df_result = df_result.drop_duplicates(subset=['content'])

# Save the final DataFrame if needed
df_result.to_csv('final_result.csv',sep='\t', encoding='utf-8-sig', index=False)

df_result['source'].value_counts()