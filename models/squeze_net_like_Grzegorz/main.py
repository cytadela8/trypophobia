import sys
sys.path.insert(0, "/input/") #for
sys.path.insert(0, "../common/") #for local
import common

from keras.models import Model
from keras.layers import *

sq1x1 = "squeeze1x1"
exp1x1 = "expand1x1"
exp3x3 = "expand3x3"
relu = "relu_"
def fire_module(x, fire_id, squeeze=16, expand=64):
    s_id = 'fire' + str(fire_id) + '/'

    if K.image_data_format() == 'channels_first':
        channel_axis = 1
    else:
        channel_axis = 3

    x = Conv2D(squeeze, (1, 1), padding='valid', name=s_id + sq1x1)(x)
    x = Activation('relu', name=s_id + relu + sq1x1)(x)

    left = Conv2D(expand, (1, 1), padding='valid', name=s_id + exp1x1)(x)
    left = Activation('relu', name=s_id + relu + exp1x1)(left)

    right = Conv2D(expand, (3, 3), padding='same', name=s_id + exp3x3)(x)
    right = Activation('relu', name=s_id + relu + exp3x3)(right)

    x = concatenate([left, right], axis=channel_axis, name=s_id + 'concat')
    return x


img_input = Input(shape=(common.resolution_x, common.resolution_y, 3))

x = Conv2D(64, (3, 3), strides=(2, 2), padding='valid', name='conv1')(img_input)
x = Activation('relu', name='relu_conv1')(x)
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool1')(x)

x = fire_module(x, fire_id=2, squeeze=16, expand=64)
x = fire_module(x, fire_id=3, squeeze=16, expand=64)
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool3')(x)

x = fire_module(x, fire_id=4, squeeze=32, expand=128)
x = fire_module(x, fire_id=5, squeeze=32, expand=128)
x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool5')(x)

x = Dropout(0.5)(x)

#x = fire_module(x, fire_id=6, squeeze=48, expand=192)
#x = fire_module(x, fire_id=7, squeeze=48, expand=192)
#x = fire_module(x, fire_id=8, squeeze=64, expand=256)
#x = fire_module(x, fire_id=9, squeeze=64, expand=256)
#x = Dropout(0.5, name='drop9')(x)

x = Conv2D(2, (1, 1), padding='valid', name='conv10')(x)
x = Activation('relu', name='relu_conv10')(x)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
x = Dense(16)(x)
x = Activation('relu', name="asdsasdcccc")(x)

x = Dense(2)(x)
out = Activation('softmax', name="asdsasd")(x)

model = Model(img_input, out, name='errrr')
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

common.experiment(model)
