# -*- coding: utf-8 -*-
"""LSTM curr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lTeIsheViP49wP3VgRTiC4820_84Jvo6
"""

pip install fxcmpy

pip install python_socketio

import datetime as dt
import pandas as pd
import numpy as np
import random
from collections import deque
from sklearn import preprocessing
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import math
import time

import fxcmpy
import datetime as dt
TOKEN = "6a23102c5f4044b4439fd0eb778f0f93a4d4d421"
con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error')
start = dt.datetime(2000, 1, 1)
stop = dt.datetime(2020, 5, 1)
df = con.get_candles('EUR/USD', period='D1', start=start, stop=stop)
df.drop(["bidopen"], axis=1, inplace=True)
df.drop(["bidclose"], axis=1, inplace=True)
df.drop(["bidhigh"], axis=1, inplace=True)
df.drop(["bidlow"], axis=1, inplace=True)
df.drop(["tickqty"], axis=1, inplace=True)
df.rename(columns={"askclose" : "close","askopen" : "open", "askhigh": "high", "asklow": "low"}, inplace=True)
df.reset_index(inplace=True)
df.drop(["date"], axis=1, inplace=True)
df.columns = [''] * len(df.columns)
df

"""PART 1"""

seq_len = 30

training = df[df.index<=4288].copy()
testing = df[df.index>4288].copy()

trainingg = training.values
x_train = []
y_train = []

for i in range(seq_len, trainingg.shape[0]):
  x_train.append(trainingg[i-30:i])
  y_train.append(trainingg[i,1])


x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0] * x_train.shape[1], 4))
y_train = np.reshape(y_train, (y_train.shape[0] , 1))

scalarx = MinMaxScaler()
scalary = MinMaxScaler()
x_train = scalarx.fit_transform(x_train)
y_train = scalary.fit_transform(y_train)

x_train = np.reshape(x_train, (4259, 30, 4))
y_train = np.reshape(y_train, (y_train.shape[0] ,))

reg = Sequential()
reg.add(LSTM(units = 120, activation= 'relu', return_sequences=True, input_shape = (x_train.shape[1], x_train.shape[2])))
reg.add(Dropout(0.2))

reg.add(LSTM(units = 240, activation= 'relu', return_sequences=True))
reg.add(Dropout(0.2))

reg.add(LSTM(units = 240, activation= 'relu', return_sequences=True))
reg.add(Dropout(0.2))

reg.add(LSTM(units = 120, activation= 'relu'))
reg.add(Dropout(0.2))

reg.add(Dense(units = 1))

reg.compile(optimizer='adam', loss = 'mean_squared_error')
reg.fit(x_train, y_train, epochs=1, batch_size=32)

past_30 = training.tail(30)
testingg = past_30.append(testing, ignore_index = True)

testinggg = testingg.values
x_test = []
y_test = []
for i in range(seq_len, testinggg.shape[0]):
  x_test.append(testinggg[i-30:i])
  y_test.append(testinggg[i,1])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0] * x_test.shape[1], 4))

inputs = scalarx.transform(x_test)

inputs = np.reshape(inputs, (1072, 30, 4))

y_pred = reg.predict(inputs)

predict = scalary.inverse_transform(y_pred)
predict = np.reshape(predict,(predict.shape[0] ,))

#VISUALIZE

plt.figure(figsize = (18,6))
plt.plot(y_test, color = 'red')
plt.plot(predict,color = 'green')
plt.legend()
plt.show()