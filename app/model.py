import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

DATA_PATH = r'C:\Users\Ev\Desktop\RedWineAnalysis\winequality-red.csv'

# Load the dataset
data = pd.read_csv(DATA_PATH)

# Select features and target variable
X = data[['density', 'residual sugar', 'alcohol']]  # Feature columns
y = data['quality']  # Target variable

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Save the trained model
joblib.dump(model, 'wine_quality_model.pkl')
