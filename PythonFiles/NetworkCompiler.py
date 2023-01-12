import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import compute_class_weight

# Read .csv and remove direction adjacent vars as they have potential NaN
df = pd.read_csv("finaldataexport.csv", index_col=[0])
df.drop(columns=['direction_directionality_index', 'direction_peak_wave_direction'], inplace=True)
print(df.head())

# Ensure that no NaN can make it in the dataframe
df = df.fillna(0)

# Convert rogue_data into binary categories
nrDF = []
for x in df['rogue_data']:
  if x > .0003:
    nrDF.append(1)
  else:
    nrDF.append(0)
df['rogue_data'] = nrDF

# Store new binary rogue_data but remove it from the dataframe to keep only training x_vars
rogueData = df['rogue_data']
df.drop(columns=['rogue_data'], inplace=True)
X = df.values
y = rogueData.values

# Define the training vars, set train size to .9 proportion of all data and validation to .1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Fit the scaler to the training data
scaler = StandardScaler()
scaler.fit(X_train)

# Scale the training and test data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the model
model = tf.keras.Sequential()

# Define the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dropout(.2, input_shape=(15,)))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu')) 
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(
  optimizer=tf.keras.optimizers.Adadelta(0.0005), 
  loss=tf.keras.losses.BinaryCrossentropy(), 
  metrics=tf.keras.metrics.BinaryAccuracy()
  )

# Create callbacks for the model to save it
my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2),
    tf.keras.callbacks.ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
]

# Compute classWeight to ensure that the network doesn't just guess 0 every time
classWeight = compute_class_weight('balanced', classes=[0,1], y=y_train) 
classWeight = dict(enumerate(classWeight))

# Fit the model
model.fit(
  X_train_scaled, 
  y_train, 
  epochs=15, 
  batch_size=8, 
  validation_data=(X_test_scaled, y_test), 
  class_weight=classWeight, 
  callbacks=my_callbacks
  )
