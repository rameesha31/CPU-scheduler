import pandas as pd

data = {
    'pid': [1,2,3,4,5],
    'arrival_time': [0,2,4,6,8],
    'burst_time': [10,5,2,8,6],
    'priority': [3,1,4,2,5],
    
}
pd_df=pd.DataFrame(data)
# Save DataFrame to CSV
csv_file_path = 'processes.csv'
pd_df.to_csv(csv_file_path, index=False)

print("CSV file saved successfully at:", csv_file_path)