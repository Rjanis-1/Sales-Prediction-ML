# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16QDtuxTtpHFJ0rSrgYZ7U7d-nTdInj9Q
"""

!pip install tensorflow keras torch torchvision opencv-python numpy pandas matplotlib

import tensorflow as tf
import matplotlib.pyplot as plt

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Display a few images
fig, axes = plt.subplots(1, 5, figsize=(10, 5))
for i in range(5):
    axes[i].imshow(x_train[i], cmap='gray')
    axes[i].axis('off')

plt.show()

!pip install pandas numpy matplotlib seaborn scikit-learn xgboost

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

!pip install kaggle kagglehub

from google.colab import files
uploaded = files.upload()

import zipfile
import os

# Extract the uploaded ZIP file
zip_file = "retail-store-sales-dirty-for-data-cleaning.zip"  # Change filename if needed
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall("dataset")  # Extract to 'dataset' folder

print("Files extracted successfully!")



import os
print(os.listdir())

import zipfile

# Extract the uploaded ZIP file
with zipfile.ZipFile("archive.zip", 'r') as zip_ref:
    zip_ref.extractall("dataset")  # Extract into 'dataset' folder

print("Files extracted successfully!")

import os

print(os.listdir("dataset"))  # List extracted files

import pandas as pd

# Load dataset
df = pd.read_csv("dataset/retail_store_sales.csv")

# Display first 5 rows
print(df.head())

# Check dataset information
print(df.info())

print(df.isnull().sum())  # Count missing values in each column

df = df.drop_duplicates()
print("Duplicate rows removed!")

import matplotlib.pyplot as plt

df.boxplot(figsize=(12, 6))
plt.xticks(rotation=45)
plt.show()

print(df.describe())  # Show statistics for numerical columns

print(df.isnull().sum())  # Show missing values count per column

df = df.dropna()
print("Missing values removed!")

# Fill numerical columns with the mean
df.fillna(df.mean(), inplace=True)

# Fill categorical columns with the most frequent value
df.fillna(df.mode().iloc[0], inplace=True)

print(df.isnull().sum())  # Should now be 0

import numpy as np

# Define function to remove outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Apply to numerical columns
for col in df.select_dtypes(include=np.number).columns:
    df = remove_outliers(df, col)

print("Outliers removed!")

df.boxplot(figsize=(12, 6))
plt.xticks(rotation=45)
plt.show()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[df.select_dtypes(include=np.number).columns] = scaler.fit_transform(df.select_dtypes(include=np.number))

print("Feature scaling applied!")

print(df.columns)

X = df.drop(columns=["Sales"])  # Features
y = df["Sales"]  # Target variable

print(df.columns)

X = df.drop(columns=["Total Spent"])  # Features
y = df["Total Spent"]  # Target variable

X = pd.get_dummies(X, drop_first=True)

X["Transaction Date"] = pd.to_datetime(X["Transaction Date"]).astype(int) / 10**9  # Convert to timestamp

print(df.columns)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns)  # Check cleaned column names

df["transaction_date"] = pd.to_datetime(df["transaction_date"]).astype(int) / 10**9

X = df.drop(columns=["total_spent"])  # Features
y = df["total_spent"]  # Target variable
X = pd.get_dummies(X, drop_first=True)  # Convert categorical data

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")

from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

# Evaluate performance
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest - MAE: {mae_rf}")
print(f"Random Forest - MSE: {mse_rf}")
print(f"Random Forest - R² Score: {r2_rf}")

import matplotlib.pyplot as plt
import seaborn as sns

# Get feature importance from Random Forest
feature_importance = pd.Series(rf_model.feature_importances_, index=X.columns)
feature_importance.sort_values(ascending=False).plot(kind='bar', figsize=(10,5))
plt.title("Feature Importance")
plt.show()

plt.figure(figsize=(12, 6))  # Increase figure size
feature_importance.sort_values(ascending=False).plot(kind='bar')
plt.title("Feature Importance")
plt.xticks(rotation=45)  # Rotate labels for better visibility
plt.show()

feature_importance.sort_values().plot(kind='barh', figsize=(10, 6))
plt.title("Feature Importance")
plt.show()

top_features = feature_importance.sort_values(ascending=False).head(10)
top_features.plot(kind='barh', figsize=(10, 6), color='skyblue')
plt.title("Top 10 Feature Importances")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.gca().invert_yaxis()  # Flip y-axis for better readability
plt.show()

numeric_features = feature_importance.loc[~feature_importance.index.str.contains('category_')]
numeric_features.sort_values(ascending=False).plot(kind='barh', figsize=(12, 8), color='steelblue')
plt.title("Feature Importance (Filtered)")
plt.show()