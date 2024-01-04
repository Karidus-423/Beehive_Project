import pandas as pd
import matplotlib.pylab as plt 
import numpy as np


df = pd.read_csv('temperature_schwartau.csv')

# Assuming your CSV file has columns 'timestamp' and 'temperature'
# You can access these columns using df['column_name']

# Convert the 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

start_time = df['timestamp'].min()
end_time = df['timestamp'].max()
interpolation_times = pd.date_range(start_time, end_time, freq='3T')

linear_interpolation= np.interp(interpolation_times, df['timestamp'], df['temperature'])

# Create the plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

# Plot the original 'temperature' data
plt.plot(df['timestamp'], df['temperature'], marker='o', linestyle='-', label='Original Data')

# Plot the linear interpolation data
plt.plot(interpolation_times, interpolated_temperature, linestyle='*', label='Linear Interpolation')

# Customize the plot
plt.title('Temperature Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.legend()  # Add a legend to differentiate lines

# Display the plot
plt.grid()
plt.tight_layout()
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.show()