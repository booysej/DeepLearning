# -*- coding: utf-8 -*-
"""MLP-Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QEEJ5b0zUVrPSJKJR8DHwwyMiicTS_km
"""

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston

boston = load_boston()
df = pd.DataFrame(boston.data, columns = boston.feature_names)
df['target'] = boston.target
df

print(boston.DESCR)

X,y = boston.data, boston.target

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2)

X_train = torch.tensor(X_train).float()
X_test = torch.tensor(X_test).float()
y_train = torch.tensor(y_train).float().unsqueeze(1)
y_test = torch.tensor(y_test).float().unsqueeze(1)

mean = X_train.mean(dim=0)
std = X_train.std(dim=0)
X_train = (X_train-mean)/std
X_test = (X_test-mean)/std

"""**Linear Regression Model**"""

class LinearRegression(nn.Module):
  def __init__(self,input_size,output_size):
    super().__init__()
    self.fc = nn.Linear(13,128,bias = True)  # Define the hidden layer
    self.out = nn.Linear(128,1,bias = True)  # Define the output layer
    self.relu = nn.ReLU()        # Define the activation function

  def forward(self,x):
    x = self.fc(x)
    x = self.relu(x)
    x = self.out(x)
    return x

model = LinearRegression(input_size = X_train.shape[1],output_size=1)
#X_train.shape[1]

criterion = nn.MSELoss()  # nn.L1Loss
optimizer = optim.SGD(model.parameters(),lr = 0.01)

"""**Training**"""

losses = []
num_epochs = 100000
for epoch in range(num_epochs):
  #Forward pass
  y_pred = model(X_train)
  loss = criterion(y_pred,y_train)

  #Backward Pass
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()


  if (epoch + 1) % 100 == 0:
    print(f'Epoch [{epoch + 1}/100000], Loss: {loss.item(): .4f}')
  losses.append(loss.item())

import matplotlib.pyplot as plt
plt.plot(range(100000),losses)
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Loss over itrations')
plt.show()

"""**Testing**"""

with torch.no_grad():
  y_test_pred = model(X_test)
  test_loss = criterion(y_test_pred,y_test)
  print(f'Test Loss: {test_loss.item():.4f}')

mae = torch.abs(y_test_pred - y_test).mean()
print('Mean Absolute Error:',mae.item())

def mean_absolute_percentage_error(y_true,y_prediction):
  return 100 * torch.mean(torch.abs((y_true-y_prediction) / y_true))

mape = mean_absolute_percentage_error(y_test,y_test_pred)
print(mape)