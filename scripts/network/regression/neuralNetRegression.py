import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

# Assumes only the used data is passed!

column_names = ["temperature","windSpeed","humidity","precipIntensity","p1"]

path = "mladostFinal-normalized"

raw_dataset = pd.read_csv(path, names= column_names, na_values = "?", comment = '\t', sep=" ")

dataset = raw_dataset.copy()
print(dataset.tail())

dataset = dataset.dropna()

train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_labels = train_dataset.pop('p1')
test_labels = test_dataset.pop('p1')

def build_model():
  model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

EPOCHS = 500

history = model.fit(
  train_dataset, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=1,
 )
model.save_weights('./checkpoints/my_checkpoint')

#model.load_weights('./checkpoints/my_checkpoint')

# Evaluate the model
loss, mae, mse = model.evaluate(test_dataset,  test_labels, verbose=1)
print("Testing set Mean Abs Error: {:5.2f} ".format(mae))
