import serial
import csv
from datetime import datetime
import os

# set baud rate
baud_rate = 9600

csv_name = 'room_data.csv'
csv_path = os.path.abspath(csv_name)

#Open a csv file
logging = open(csv_name, mode='w', newline='', encoding='utf-8')
writer = csv.writer(logging)

# Open a serial port that is connected to an Arduino
ser = serial.Serial('COM3', baud_rate, timeout=5)
ser.flushInput()

# Write CSV headers
writer.writerow(['Timestamp', 'Humidity (%)', 'Temperature (°C)'])

print("Collecting data... Press Ctrl+C to stop.")

try:
    while True:

        # Read in data from Serial until a new line is received
        ser_bytes = ser.readline()
        # Convert received bytes into text format
        decoded_bytes = ser_bytes.decode("utf-8").strip()

        if decoded_bytes:

            # Split received sensor data
            sensor_data = decoded_bytes.split(',')

            if len(sensor_data) == 2:

                # Retrieve current time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                print(current_time, sensor_data[0], sensor_data[1])

                # Write data to CSV file
                writer.writerow([
                    current_time,
                    sensor_data[0],
                    sensor_data[1]
                ])

except KeyboardInterrupt:
    print("\nFinished collecting data.")

# Close serial port and CSV file
ser.close()
logging.close()

print(f"CSV saved to: {csv_path}")
print("Logging finished")