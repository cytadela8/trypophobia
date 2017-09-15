import sys

sys.path.insert(0, "/input/") #for cloud
sys.path.insert(0, "../common/") #for local
import common

from keras.models import Model
from keras.layers import *

img_input = Input(shape=(common.resolution_x, common.resolution_y, 3))
x = Conv2D(8, (3, 3), padding='same')(img_input)
x = Activation('relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(16, (3, 3), padding='same')(x)
x = Activation('relu')(x)
x = Dropout(0.15)(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = Activation('relu')(x)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(24, (3, 3), padding='same')(x)
x = Activation('relu')(x)
x = Dropout(0.2)(x)
x = Conv2D(12, (3, 3), padding='same')(x)
x = Dropout(0.25)(x)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(32, (3, 3), padding='same')(x)
x = Activation('relu')(x)
x = Dropout(0.25)(x)
x = Conv2D(16, (3, 3), padding='same')(x)
x = Activation('relu')(x)
x = Dropout(0.3)(x)
x = BatchNormalization()(x)
x1 = GlobalAveragePooling2D()(x)
x2 = GlobalMaxPooling2D()(x)
x = Concatenate()([x1, x2])
x = Dense(16)(x)
x = Activation('relu')(x)
x = Dense(2)(x)
output = Activation('softmax')(x)
model = Model(img_input, output)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

common.experiment(model)
