import json
import pandas as pd
import time

def resample_data(data, freq='10ms'):
    # Convert JSON data to DataFrame
    df = pd.json_normalize(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # Generate a date range with the desired frequency
    time_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq=freq)
    
    # Reindex the dataframe to the new time_index and interpolate missing values
    df = df.infer_objects()
    df_resampled = df.reindex(time_index).interpolate(method='linear')
    
    # Fill missing device_id with the previous value
    df_resampled['device_id'] = df_resampled['device_id'].fillna(method='ffill')
    
    # Round the values according to the specified precision
    if 'temperature' in df_resampled.columns:
        df_resampled['temperature'] = df_resampled['temperature'].apply(lambda x: format(x, '.2f'))
    for column in df_resampled.columns:
        if 'acceleration' in column and df_resampled[column].dtype == 'float64':
            df_resampled[column] = df_resampled[column].apply(lambda x: format(x, '.3f'))
        elif 'gyroscope' in column and df_resampled[column].dtype == 'float64':
            df_resampled[column] = df_resampled[column].apply(lambda x: format(x, '.7f'))
    
    # Reset index to make timestamp a column again
    df_resampled.reset_index(inplace=True)
    df_resampled.rename(columns={'index': 'timestamp'}, inplace=True)
    
    # Convert timestamp to string to make it JSON serializable
    df_resampled['timestamp'] = df_resampled['timestamp'].astype(str)
    
    # Convert DataFrame back to JSON
    resampled_data = df_resampled.to_dict(orient='records')
    return resampled_data

def main():
    input_file = 'sensordata.json'
    output_file = 'resampled_sensordata.json'
    
    while True:
        # Read the sensor data file
        with open(input_file, 'r') as file:
            data = json.load(file)
        
        # Resample the data
        resampled_data = resample_data(data)
        
        # Write the resampled data to a new file
        with open(output_file, 'w') as file:
            json.dump(resampled_data, file, indent=4)
        
        # Wait for 6 seconds before the next iteration
        time.sleep(6)

if __name__ == "__main__":
    main()
