import pandas as pd
import numpy as np

# Load simulated sensor and session data
df = pd.read_csv('simulated_raw_data.csv')

print("Initial data shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

# Convert timestamp
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Check sensor values
temperature_errors = (
    (df['Temperature (°C)'] < 0) |
    (df['Temperature (°C)'] > 50)
)

humidity_errors = (
    (df['Humidity (%)'] < 0) |
    (df['Humidity (%)'] > 100)
)

print("\nTemperature errors:", temperature_errors.sum())
print("Humidity errors:", humidity_errors.sum())

# Remove invalid temp and humidity readings
df = df[
    (df['Temperature (°C)'] >= 0) &
    (df['Temperature (°C)'] <= 50) &
    (df['Humidity (%)'] >= 0) &
    (df['Humidity (%)'] <= 100)
]

# Add time variables
df['Hour'] = df['Timestamp'].dt.hour
df['Day_of_Week'] = df['Timestamp'].dt.day_name()

# Aggregate data by session
processed_df = df.groupby('Session').agg(
    Timestamp=('Timestamp', 'first'),

    # Temperature statistics
    **{
        'Mean Temperature (°C)': ('Temperature (°C)', 'mean'),
        'Min Temperature (°C)': ('Temperature (°C)', 'min'),
        'Max Temperature (°C)': ('Temperature (°C)', 'max'),
        'Temperature SD': ('Temperature (°C)', 'std'),

        # Humidity statistics
        'Mean Humidity (%)': ('Humidity (%)', 'mean'),
        'Min Humidity (%)': ('Humidity (%)', 'min'),
        'Max Humidity (%)': ('Humidity (%)', 'max'),

        # Session results
        'Focus Rating': ('Focus Rating', 'first'),
        'Mean Reaction Time (ms)': (
            'Mean Reaction Time (ms)',
            'first'
        )
    }
).reset_index()

# Round environmental values to 2 decimal places
processed_df = processed_df.round({
    'Mean Temperature (°C)': 2,
    'Min Temperature (°C)': 2,
    'Max Temperature (°C)': 2,
    'Temperature SD': 2,
    'Mean Humidity (%)': 2,
    'Min Humidity (%)': 2,
    'Max Humidity (%)': 2
})

# Format timestamp
processed_df['Timestamp'] = processed_df[
    'Timestamp'
].dt.strftime('%Y-%m-%d %H:%M:%S')

# Keep column order
processed_df = processed_df[
    [
        'Session',
        'Timestamp',
        'Mean Humidity (%)',
        'Mean Temperature (°C)',
        'Min Temperature (°C)',
        'Max Temperature (°C)',
        'Temperature SD',
        'Min Humidity (%)',
        'Max Humidity (%)',
        'Focus Rating',
        'Mean Reaction Time (ms)'
    ]
]

# Display processed data
print("\nProcessed data:")
print(processed_df)

print("\nFinal shape:")
print(processed_df.shape)

print("\nFinal missing values:")
print(processed_df.isnull().sum())

# Export processed data
processed_df.to_csv(
    'processed_session_data.csv',
    index=False
)

print("\nProcessed data saved to:")
print("processed_session_data.csv")
