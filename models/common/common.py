import math

import keras
from PIL import Image
from keras.callbacks import Callback
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
    print("Number of photos in %s: %s" % (folder, il))
    print((il // math.ceil(il / 50)) * "_")
    for file in os.listdir(folder):
        image = cv2.imread(os.path.join(folder, file))
        if image is not None:

            height, width, channels = image.shape
            if height != resolution_x or width != resolution_y:
                image = cv2.resize(image, (resolution_x, resolution_y), interpolation=cv2.INTER_LINEAR)
                print("Resizing image with shape %s" % image.shape)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images.append(image)
        if i % math.ceil(il / 50) == 0:
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
    def __init__(self, X_test, Y_test, images_per_epoch=-1):
        self.epoch_id = 0
        self.images_per_epoch = images_per_epoch
        self.X_test = X_test
        self.Y_test = Y_test

    def on_epoch_end(self, epoch, logs={}):
        self.epoch_id += 1

        # Predict the digits for images of the test set.
        validation_predictions = self.model.predict_classes(self.X_test)
        scores = self.model.predict(self.X_test)

        # Identify the incorrectly classified images and send them to Neptune Dashboard.
        image_per_epoch = 0
        for index, (prediction, actual) in enumerate(zip(validation_predictions, self.Y_test.argmax(axis=1))):
            if prediction != actual:
                if image_per_epoch == self.images_per_epoch:
                    break
                image_per_epoch += 1

                ctx.job.channel_send('false_predictions', neptune.Image(
                    name='[{}] pred: {} true: {}'.format(self.epoch_id, prefiction_names[prediction],
                                                         prefiction_names[actual]),
                    description="{} {:5.1f}%".format(prefiction_names[0], 100 * scores[index][0]),
                    data=array_3d_to_image(self.X_test[index, :, :, :])))

def experiment(model):
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
    with open(os.path.join(ctx.params.output_location, 'model.json'), 'w') as f:
        f.write(model.to_json())
    model.save(os.path.join(ctx.params.output_location, "model_notlearned"))

    print("Fitting started")
    history = model.fit(X_train, Y_train,
                        epochs=ctx.params.number_of_epochs,
                        batch_size=ctx.params.batch_size,
                        validation_data=(X_test, Y_test), callbacks=[
            keras.callbacks.ModelCheckpoint(os.path.join(ctx.params.output_location, "modelweights.{epoch:02d}-{val_loss:.2f}.hdf5"), monitor='val_loss', verbose=0,
                                    save_best_only=False, save_weights_only=True, mode='auto', period=1),
            keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=15, verbose=0, mode='auto'),
            NeptuneCallback(X_test, Y_test, images_per_epoch=10)])

    model.save(os.path.join(ctx.params.output_location, "model"))
    model.save_weights(os.path.join(ctx.params.output_location, "model_weights"))

    with open(os.path.join(ctx.params.output_location, 'model.json'), 'w') as f:
        f.write(model.to_json())
