# -*- coding: utf-8 -*-
"""Redes_No_Lineal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b-WKBvM0o-PxzMzQx619pb-hA4GD3FQ1
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import KFold

# Load the data
data = pd.read_csv("bmi.csv", sep=",")
gender_dummie = pd.get_dummies(data['Gender'], drop_first=True)
gender = gender_dummie.values.reshape(-1)
height = data['Height']
weight = data['Weight']
bmi = data['Index']

random_state = 42
np.random.seed(random_state)
noise = np.random.normal(0, 1, len(data))
data['Height'] = data['Height'] + noise/100
data['Weight'] = data['Weight'] + noise

X = np.array([gender, height, weight]).T
y = bmi + noise

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Visualize data
print(data.head())
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_train[:,1], X_train[:,2], y_train, label='Train data')
ax.scatter(X_test[:,1], X_test[:,2], y_test, label='Test data')
ax.set_title('Datos de prueba y entrenamiento')
ax.set_xlabel('Height')
ax.set_ylabel('Weight')
ax.set_zlabel('BMI')
ax.legend()
plt.show()

# Create the neural network model
def create_model(n_neurons):
    model = MLPRegressor(hidden_layer_sizes=(n_neurons, 2*n_neurons, 2*n_neurons, n_neurons), activation='relu', random_state=42)
    return model

train_mse = []
test_mse = []

for n_neurons in np.arange(1, 600, 25):
  model = create_model(n_neurons)
  model.fit(X_train, y_train)

  y_model_train = model.predict(X_train)
  y_model_test = model.predict(X_test)

  train_mse.append(mean_squared_error(y_model_train, y_train))
  test_mse.append(mean_squared_error(y_test, y_model_test))

plt.figure()
plt.plot(np.arange(1, 600, 25), train_mse, label='Training Error', marker='.')
plt.plot(np.arange(1, 600, 25), test_mse, label='Test Error', marker='.')
#plt.plot(test_mse + train_mse, label='Total error', marker='o')
plt.xlabel('Neural density in hidden layer')
plt.ylabel('Mean Squared Error')
plt.title('MSE vs Neural density')
plt.ylim([40,100])
plt.xlim([0,325])
plt.legend()
plt.grid()
plt.show()

# Define the hyperparameters and their possible values
layer_sizes = []
for n_neurons in np.arange(1, 600, 25):
  layer_sizes.append((n_neurons, 2*n_neurons, 2*n_neurons, n_neurons))

param_grid = {
    'hidden_layer_sizes': layer_sizes,
    'activation': ['relu'],
    'solver': ['adam'],
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

y_pred_test = best_model.predict(X_test)
y_pred_train = best_model.predict(X_train)
mse_test = mean_squared_error(y_test, y_pred_test)
mse_train = mean_squared_error(y_train, y_pred_train)

print(f"Mean Squared Error en Test Set: {mse_test}")
print(f"Mean Squared Error en Train Set: {mse_train}")
print("Mejores hiperparámetros: ", grid_search.best_params_)

# Visualize data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,1], X[:,2], y, label='Origina data')
ax.scatter(X_test[:,1], X_test[:,2], y_pred_test, label='Predicted data')
ax.set_title('Datos y datos predichos')
ax.set_xlabel('Height')
ax.set_ylabel('Weight')
ax.set_zlabel('BMI')
ax.legend()
plt.show()

