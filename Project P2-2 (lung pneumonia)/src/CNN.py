import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras import callbacks
from keras.preprocessing.image import ImageDataGenerator #image generator label data based on the dir the image in contained in
from tensorflow.keras.optimizers import RMSprop
from keras.preprocessing import image
def CNN():
    train_datagen = ImageDataGenerator(rescale=1 / 255)
    test_datagen = ImageDataGenerator(rescale=1 / 255)

    train_data = train_datagen.flow_from_directory(
        'C:/Users/Vukasin/Desktop/chest_xray_data_set/train',
        target_size=(256,256),
        batch_size=32,
        class_mode='categorical',
        classes = ['VIRUS','NORMAL','BACTERIA']
    )

    test_data = test_datagen.flow_from_directory(
        'C:/Users/Vukasin/Desktop/chest_xray_data_set/test',
        target_size=(256,256),
        batch_size=32,
        class_mode='categorical',
        classes=['VIRUS', 'NORMAL', 'BACTERIA']
    )

    model = tf.keras.models.Sequential([

        # 1
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(256, 256, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 2
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 3
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 4
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 5
        tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 6
        # tf.keras.layers.Conv2D(512, (3, 3), activation='relu'),
        # tf.keras.layers.MaxPooling2D(2, 2),
        # tf.keras.layers.Dropout(0.2),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    callback = tf.keras.callbacks.LearningRateScheduler(scheduler)
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(0.0001,momentum=0.9), metrics=['accuracy'],callbacks=callback)

    model.summary()

    history = model.fit(
            train_data,
            #steps_per_epoch =54,
            epochs = 29,
            validation_data = test_data
    )

def scheduler(epoch, lr):
  if epoch < 10:
    return 0.0001
  if epoch < 20:
    return 0.00001
  if epoch < 30:
    return 0.000001

if __name__ == '__main__':
    CNN()