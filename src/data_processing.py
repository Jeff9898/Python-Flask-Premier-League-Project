import pandas as pd

# Load data from CSV
players_df = pd.read_csv('players_data.csv')  # Adjust the path if necessary

# Display the first few rows of the DataFrame
print("First few rows of the data:")
print(players_df.head())

# Display summary statistics
print("\nSummary statistics:")
print(players_df.describe())

# Check for missing values
print("\nMissing values in each column:")
print(players_df.isnull().sum())


# Data Cleaning and Feature Selection
# Assuming you want to keep relevant columns like 'goals_scored', 'assists', 'minutes', 'total_points'

# Dropping rows with missing target values (if any)
players_df = players_df.dropna(subset=['total_points'])

# Select relevant features
features = players_df[['goals_scored', 'assists', 'minutes']]
target = players_df['total_points']

print("\nSelected features:")
print(features.head())
print("\nTarget values:")
print(target.head())
