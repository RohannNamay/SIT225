import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Reproducible simulation
np.random.seed(42)

# Simulation settings
num_sessions = 30
session_duration_minutes = 30
sampling_interval_seconds = 30

# Starting timestamp
start_datetime = datetime(2026, 9, 1, 9, 0, 0)

raw_data = []

for session in range(1, num_sessions + 1):

    # Start time for this session
    session_start = start_datetime + timedelta(
        days=session - 1
    )

    # Simulate room conditions with arbitrary values
    base_temperature = np.random.normal(22.0, 0.8)
    base_humidity = np.random.normal(55.0, 4.0)

    temperatures = []
    humidities = []

    # 30 minutes at 30-second intervals = 60 readings
    num_readings = int(
        session_duration_minutes * 60 / sampling_interval_seconds
    )

    for reading in range(num_readings):

        timestamp = session_start + timedelta(
            seconds=reading * sampling_interval_seconds
        )

        # Small random variation during the session
        temperature = base_temperature + np.random.normal(0, 0.08)
        humidity = base_humidity + np.random.normal(0, 0.5)

        temperatures.append(temperature)
        humidities.append(humidity)

    # Simulate focus rating
    focus_rating = np.random.normal(7.0, 1.2)
    focus_rating = int(
        np.clip(round(focus_rating), 1, 10)
    )

    # Simulate five reaction time readings
    reaction_times = np.random.normal(230, 12, 5)

    # Calculate the mean reaction time
    mean_reaction_time = int(
        round(
            np.mean(
                np.clip(reaction_times, 180, 350)
            )
        )
    )

    # Add all sensor readings for this session
    # The focus rating and reaction time are repeated
    # for each reading from the same session.
    for reading in range(num_readings):

        timestamp = session_start + timedelta(
            seconds=reading * sampling_interval_seconds
        )

        temperature = temperatures[reading]
        humidity = humidities[reading]

        raw_data.append([
            session,
            timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            round(humidity, 2),
            round(temperature, 2),
            focus_rating,
            mean_reaction_time
        ])

# Create one DataFrame
df = pd.DataFrame(
    raw_data,
    columns=[
        'Session',
        'Timestamp',
        'Humidity (%)',
        'Temperature (°C)',
        'Focus Rating',
        'Mean Reaction Time (ms)'
    ]
)

# Save one CSV file
df.to_csv(
    'simulated_raw_data.csv',
    index=False
)

print("Simulation complete.")
print()
print("File created:")
print("simulated_raw_data.csv")
print()
print("Number of sessions:", num_sessions)
print("Readings per session:", num_readings)
print("Total rows:", len(df))
print()
print("Columns:")
print(df.columns.tolist())

