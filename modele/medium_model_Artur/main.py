import math

import keras
from PIL import Image
from keras.callbacks import Callback
from keras.models import Sequential
from keras.layers import *
import numpy as np
import os
import cv2
from deepsense import neptune

ctx = neptune.Context()

ctx.job.integrate_with_keras()

resolution_x = ctx.params.resolution_x
resolution_y = ctx.params.resolution_y

prefiction_names = ["trypo", "normal"]


def load_folder(folder):
    images = []
    i = 0
    il = len(os.listdir(folder))
    print ("Number of photos in %s: %s" % (folder, il))
    print ((il//math.ceil(il/50))*"_")
    for file in os.listdir(folder):
        image = cv2.imread(os.path.join(folder, file))
        if image is not None:

            height, width, channels = image.shape
            if height != resolution_x or width != resolution_y:
                image = cv2.resize(image, (resolution_x, resolution_y), interpolation=cv2.INTER_LINEAR)
                print("Resizing image with shape %s" % image.shape)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images.append(image)
        if i % math.ceil(il/50) == 0:
            print(".", end="", flush=True)
        i += 1
    print("")
    ret = np.array(images)
    del images
    return ret


def image_to_x_y(fobia_images, normal_images):
    X_train = np.append(fobia_images, normal_images, axis=0)
    Y_train = np.array([[1, 0] for _ in range(len(fobia_images))] +
                       [[0, 1] for _ in range(len(normal_images))])
    return X_train, Y_train


def array_2d_to_image(array, autorescale=True):
    assert array.min() >= 0
    assert len(array.shape) == 2
    if array.max() <= 1 and autorescale:
        array = 255 * array
    array = array.astype('uint8')
    return Image.fromarray(array)


def array_3d_to_image(array, autorescale=True):
    assert array.min() >= 0
    assert len(array.shape) == 3
    if array.max() <= 1 and autorescale:
        array = 255 * array
    array = array.astype('uint8')
    return Image.fromarray(array, 'RGB')


class NeptuneCallback(Callback):
    def __init__(self, images_per_epoch=-1):
        self.epoch_id = 0
        self.images_per_epoch = images_per_epoch

    def on_epoch_end(self, epoch, logs={}):
        self.epoch_id += 1

        # Predict the digits for images of the test set.
        validation_predictions = model.predict_classes(X_test)
        scores = model.predict(X_test)

        # Identify the incorrectly classified images and send them to Neptune Dashboard.
        image_per_epoch = 0
        for index, (prediction, actual) in enumerate(zip(validation_predictions, Y_test.argmax(axis=1))):
            if prediction != actual:
                if image_per_epoch == self.images_per_epoch:
                    break
                image_per_epoch += 1

                ctx.job.channel_send('false_predictions', neptune.Image(
                    name='[{}] pred: {} true: {}'.format(self.epoch_id, prefiction_names[prediction], prefiction_names[actual]),
                    description="{} {:5.1f}%".format(prefiction_names[0], 100 * scores[index][0]),
                    data=array_3d_to_image(X_test[index,:,:,:])))


model = Sequential()
model.add(Conv2D(16, (3, 3), padding='same',
          input_shape=(resolution_x, resolution_y, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(24, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(24, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3), padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(GlobalAveragePooling2D())
model.add(Dropout(0.5))
for i in range(1):
    model.add(Dense(16))
    model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

base_data = ctx.params.input_location + ctx.params.data_folder
fobia_folder = base_data + "/train/trypo"
normal_folder = base_data + "/train/norm"
fobia_folder_val = base_data + "/valid/trypo"
normal_folder_val = base_data + "/valid/norm"

normal_images = load_folder(normal_folder) / 255.
normal_images_val = load_folder(normal_folder_val) / 255.
fobia_images_val = load_folder(fobia_folder_val) / 255.
fobia_images = load_folder(fobia_folder) / 255.
print("data loaded 1/2")

X_train, Y_train = image_to_x_y(fobia_images, normal_images)
del fobia_images
del normal_images
print(X_train.shape, Y_train.shape, len(X_train), len(Y_train))
assert len(X_train) == len(Y_train)
X_test, Y_test = image_to_x_y(fobia_images_val, normal_images_val)
del fobia_images_val
del normal_images_val
assert len(X_test) == len(Y_test)
print("data loaded 2/2")
with open('/output/model.json', 'w') as f:
    f.write(model.to_json())
model.save("/output/model_notlearned")

history = model.fit(X_train, Y_train,
                    epochs=ctx.params.number_of_epochs,
                    batch_size=ctx.params.batch_size,
                    validation_data=(X_test, Y_test), callbacks=[
        keras.callbacks.ModelCheckpoint("/output/modelweights.{epoch:02d}-{val_loss:.2f}.hdf5", monitor='val_loss', verbose=0,
                                save_best_only=False, save_weights_only=True, mode='auto', period=1),
        keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=15, verbose=0, mode='auto'),
        NeptuneCallback(images_per_epoch=10)
    ])

model.save("/output/model")
model.save_weights("/output/model_weights")

with open('/output/model.json', 'w') as f:
    f.write(model.to_json())
