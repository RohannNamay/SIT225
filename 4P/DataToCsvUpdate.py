```python
import serial
import csv
import pandas as pd
from datetime import datetime
import os

# set baud rate
baud_rate = 9600

# Ask for session number
session_number = int(input("Enter session number: "))

csv_name = 'room_data.csv'
csv_path = os.path.abspath(csv_name)

# Open a csv file
file_exists = os.path.exists(csv_name)

# Open a serial port that is connected to an Arduino
ser = serial.Serial('COM5', baud_rate, timeout=5)
ser.flushInput()

# Write CSV headers
if not file_exists:
    with open(
        csv_name,
        mode='a',
        newline='',
        encoding='utf-8'
    ) as logging:
        writer = csv.writer(logging)
        writer.writerow([
            'Session',
            'Timestamp',
            'Humidity (%)',
            'Temperature (°C)'
        ])

# Create a list to buffer sensor readings
data = []

print("Collecting data for 30 minutes... Press Ctrl+C to stop early")

try:
    while True:

        # Read in data from Serial until a new line is received
        ser_bytes = ser.readline()
        # Convert received bytes into text format
        try:
            decoded_bytes = ser_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            continue

        if decoded_bytes:

            # Check whether Arduino has finished
            if decoded_bytes == "COLLECTION_COMPLETE":
                print("\n30-minute collection complete.")
                break

            # Split received sensor data
            sensor_data = decoded_bytes.split(',')

            if len(sensor_data) == 2:

                try:
                    # Retrieve current time
                    current_time = datetime.now()

                    humidity = float(sensor_data[0].strip())
                    temperature = float(sensor_data[1].strip())
                except ValueError:
                    print("Invalid sensor reading:", decoded_bytes)
                    continue

                print(
                    current_time.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    ),
                    humidity,
                    temperature
                )

                # Buffer data
                data.append([
                    session_number,
                    current_time,
                    humidity,
                    temperature
                ])

except KeyboardInterrupt:
    print("\nCollection stopped manually.")

finally:

    # Convert buffered data into a Pandas DataFrame
    df = pd.DataFrame(
        data,
        columns=[
            'Session',
            'Timestamp',
            'Humidity (%)',
            'Temperature (°C)'
        ]
    )

    # Convert timestamp to the required format
    if not df.empty:
        df['Timestamp'] = df['Timestamp'].dt.strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        # Write data to CSV file
        df.to_csv(
            csv_path,
            mode='a',
            header=not file_exists,
            index=False
        )

    # Close serial port and CSV file
    ser.close()

print(f"CSV saved to: {csv_path}")
print("Logging finished.")
```
