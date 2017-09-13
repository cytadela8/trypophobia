
from keras.layers import *
from keras import *
from keras.models import *
resolution_x = 250
resolution_y = 250
import tensorflow as tf
tf.python.control_flow_ops = tf
model = Sequential()
model.add(Conv2D(16, 3, 3, border_mode='same',
          input_shape=(resolution_x, resolution_y, 3)))
#model.add(Convolution2D(8, 3, 3, border_mode='same'))
model.add(Conv2D(32, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Conv2D(32, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Dropout(0.15))
model.add(Conv2D(32, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Conv2D(64, 3, 3, border_mode='same'))
model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Dropout(0.25))
model.add(Conv2D(32, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(GlobalAveragePooling2D())
#model.add(Flatten())
#model.add(Dropout(0.2))
for i in range(1):
    model.add(Dense(16))
    model.add(Activation('relu'))
    #model.add(Dropout(0.2))
#for i in range(1):
#    model.add(Dense(32))
#    model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
with open('model.json', 'w') as f:
    f.write(model.to_json())
