# -*- coding: utf-8 -*-
"""MultiClassClassification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oue0K4YL1q20QRPcmBTCjdmGXlIRT9vd
"""

import torch
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import make_circles
from sklearn.datasets import make_blobs

device = "cuda" if torch.cuda.is_available() else "cpu"
device

import requests
from pathlib import Path

# Download helper functions from Learn PyTorch repo (if not already downloaded)
if Path("helper_functions.py").is_file():
  print("helper_functions.py already exists, skipping download")
else:
  print("Downloading helper_functions.py")
  request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py")
  with open("helper_functions.py", "wb") as f:
    f.write(request.content)

from helper_functions import plot_predictions, plot_decision_boundary

X, y = make_blobs(n_samples = 1000, centers = 4 , n_features = 2, random_state = 42, cluster_std=1.5)
X, y = torch.from_numpy(X).type(torch.float), torch.from_numpy(y).type(torch.float)

num = int(len(y)*0.8)
X_train = X[:num]
X_test = X[num:]
y_train = y[:num]
y_test = y[num:]

plt.figure(figsize=(10, 7))
plt.scatter(X[:,0], X[:,1], c = y, cmap=plt.cm.RdYlBu)

class blobModel(nn.Module):
  def __init__(self, input_features=2, output_features=4, hidden_units=8):
    super().__init__()
    self.liner_layer = nn.Sequential(
        nn.Linear(in_features = input_features, out_features = hidden_units),
        nn.Linear(in_features=hidden_units, out_features=hidden_units),
        nn.Linear(in_features=hidden_units, out_features=output_features)
    )

  def forward(self, x):
    return self.liner_layer(x)

def accuracy(y_pred, y_test):
  correct = torch.eq(y_pred, y_test).sum().item()
  return (correct/len(y_test))*100

model_4 = blobModel().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params=model_4.parameters(), lr = 0.1)

torch.manual_seed(42)

epochs = 1000

for epoch in range(epochs):
  model_4.train()

  y_logits = model_4(X_train.to(device))
  y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)

  loss = loss_fn(y_logits, y_train.to(device).long())

  acc = accuracy(y_pred, y_train.to(device))

  optimizer.zero_grad()

  loss.backward()

  optimizer.step()

  model_4.eval()

  with torch.inference_mode():
    y_test_logits = model_4(X_test.to(device))
    y_test_pred = torch.softmax(y_test_logits, dim = 1).argmax(dim=1)

    loss_test = loss_fn(y_test_logits, y_test.to(device).long())
    acc_test = accuracy(y_test_pred, y_test.to(device))

    if epoch % 10 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.5f}, Acc: {acc:.2f}% | Test Loss: {loss_test:.5f}, Test Acc: {acc_test:.2f}%")

plot_decision_boundary(model_4, X_test.to(device), y_test.to(device))