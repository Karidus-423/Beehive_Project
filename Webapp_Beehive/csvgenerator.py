import csv
import random
from datetime import datetime, timedelta

# Open a CSV file for writing
with open('upload_test_change.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    header = ["Sensor_number", "X", "Y", "Z", "Year", "Month", "Day", 
              "Hour", "Minute", "Second", "Temperature", "Timestamp"]
    writer.writerow(header)

    # Generate and write data rows for each year from 2020 to 2023
    for year in range(2020, 2024):
        for sensor_number in range(1, 55):  # Sensor_number range [1, 54]
            # Generate x, y, and z values for the current sensor number
            x = random.randint(0, 3)
            y = random.randint(0, 9)
            z = random.randint(0, 2)

            # Initialize datetime for the entire year
            current_time = datetime(year, 1, 1, 0, 0, 0)

            while current_time.year == year:  # Generate data for the specified year
                # Create a row of data with separate year, month, day, hour, minute, and second columns
                data_row = [sensor_number, x, y, z, 
                            current_time.year, current_time.month, 
                            current_time.day, current_time.hour, 
                            current_time.minute, current_time.second, 
                            round(random.uniform(32, 38), 2), 
                            current_time.strftime('%Y-%m-%d %H:%M:%S')]

                # Write the data to the CSV file
                writer.writerow(data_row)

                # Increment the time by 1 hour for the next recording
                current_time += timedelta(hours=1)

print("CSV file has been generated.")
