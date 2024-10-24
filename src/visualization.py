import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load cleaned data
players_df = pd.read_csv('players_data.csv')

# Data preparation
players_df = players_df.dropna(subset=['total_points'])
X = players_df[['goals_scored', 'assists', 'minutes']]
y = players_df['total_points']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Plot actual vs predicted values
plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel('Actual Total Points')
plt.ylabel('Predicted Total Points')
plt.title('Actual vs Predicted Total Points')
plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r')  # Diagonal line
plt.grid()
plt.show()


