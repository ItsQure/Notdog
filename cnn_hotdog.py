# -*- coding: utf-8 -*-
"""CNN_Hotdog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hcidhMvNaVydPBo2ewIoTdDY5b4IBAA5
"""

import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

from google.colab import drive
drive.mount('/content/gdrive')

!unzip gdrive/My\ Drive/archive

#ImageDataGenerator class from keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import save_img

img = load_img('/content/food-101/food-101/images/apple_pie/1005649.jpg', color_mode='grayscale')

# convert to numpy array
img_array = img_to_array(img)

newsize = (500,500)

img.resize(newsize)
img_array = img_to_array(img)

# Commented out IPython magic to ensure Python compatibility.
# %pylab inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#img = mpimg.imread('/content/food-101/food-101/images/apple_pie/1005649.jpg')
#imgplot = plt.imshow(img)
#plt.show()



"""# Read through DB and grab all images

"""

from pathlib import Path
file = open('/content/food-101/food-101/meta/classes.txt', 'r')
labelStr = file.read()
labels = labelStr.split()
counter = 0
labDict = {}
for label in labels:
  if not bool(labDict) or label not in labDict:
    labDict[label] = counter
    counter += 1
  else:
    continue

pathlist = Path('/content/food-101/food-101/').glob('**/*.jpg')
X = []
Y = []
counter = 0
for path in pathlist:
     # because path is object not string
     path_in_str = str(path)
     direct = path_in_str.split('/')
     category = direct[direct.index('food-101')+3]

     #X is pixel data 
     img = load_img(path_in_str, color_mode='grayscale')
     #resize to make images' size consistent
     newsize = (500,500)
     img = img.resize(newsize)
     #convert to list
     xArr = img_to_array(img)
     imgArr = asarray(xArr)
    # X.append(imgArr)

     #Y is categorical data
     catNum = labDict[category]
     Y.append(catNum)
     counter += 1

X = array(X)
Y = array(Y)
print(X.shape)
print(Y.shape)

classes = np.unique(Y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)

"""# Old CNN practice

"""

from keras.datasets import fashion_mnist
(train_X,train_Y), (test_X,test_Y) = fashion_mnist.load_data()

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

print('Training data shape : ', train_X.shape, train_Y.shape)

print('Testing data shape : ', test_X.shape, test_Y.shape)



# Find the unique numbers from the train labels
classes = np.unique(train_Y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

plt.figure(figsize=[9,5])

# Display the first image in training data
plt.subplot(121)
plt.imshow(train_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(train_Y[0]))

# Display the first image in testing data
plt.subplot(122)
plt.imshow(test_X[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(test_Y[0]))

print("before: " + str(train_X.shape))

train_X = train_X.reshape(-1, 28,28, 1)
test_X = test_X.reshape(-1, 28,28, 1)
train_X.shape, test_X.shape

train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X / 255.
test_X = test_X / 255.



import tensorflow as tf
from tensorflow import keras
from keras import utils

hot_train_Y = tf.keras.utils.to_categorical(train_Y)
hot_test_Y = tf.keras.utils.to_categorical(test_Y)

print(str(train_Y.shape))
print(str(hot_train_Y.shape))
print("before: " + str(train_Y[0]))
print("after: " + str(hot_train_Y[0]))

from sklearn.model_selection import train_test_split
train_X,valid_X,train_label,valid_label = train_test_split(train_X, hot_train_Y, test_size=0.2)

import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Normalization
from keras.layers import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras import optimizers

batch_size = 64
epochs = 20
num_classes = 10

fashion_model = Sequential()
fashion_model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',input_shape=(28,28,1),padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D((2, 2),padding='same'))
fashion_model.add(Dropout(.2))
fashion_model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Dropout(.2))
fashion_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))                  
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Dropout(.25))
fashion_model.add(Flatten())
fashion_model.add(Dense(128, activation='linear'))
fashion_model.add(LeakyReLU(alpha=0.1))             
fashion_model.add(Dropout(.4))     
fashion_model.add(Dense(num_classes, activation='softmax'))

fashion_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adam(),metrics=['accuracy'])

fashion_model.summary()



fashion_train = fashion_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))

fashion_model.save("mm.h5py")

fashion_model = Sequential()
fashion_model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',input_shape=(28,28,1),padding='same'))
fashion_model.add(Dropout(.1))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D((2, 2),padding='same'))
fashion_model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(Dropout(0.2))
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))                  
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Dropout(.25))
fashion_model.add(Flatten())
fashion_model.add(Dense(128, activation='linear'))
fashion_model.add(LeakyReLU(alpha=0.1))             
fashion_model.add(Dropout(.4))     
fashion_model.add(Dense(num_classes, activation='softmax'))

fashion_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adam(),metrics=['accuracy'])

fashion_train = fashion_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))

