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
    train_datagen = ImageDataGenerator(rescale=1 / 255,zoom_range=0.15, vertical_flip=True)
    test_datagen = ImageDataGenerator(rescale=1 / 255)
    all_test_datagen = ImageDataGenerator(rescale=1 / 255)

    train_data = train_datagen.flow_from_directory(
        'C:/Users/Vukasin/Desktop/chest_xray_data_set/train',
        target_size=(128,128),
        batch_size=32,
        class_mode='categorical',
        classes = ['VIRUS','NORMAL','BACTERIA']
    )

    test_data = test_datagen.flow_from_directory(

        'C:/Users/Vukasin/Desktop/chest_xray_data_set/test',
        target_size=(128,128),
        batch_size=32,
        class_mode='categorical',
        classes=['VIRUS', 'NORMAL', 'BACTERIA']
    )

    new_test_data = all_test_datagen.flow_from_directory(
        'C:/Users/Vukasin/Desktop/chest-xray-dataset-test/chest-xray-dataset-test',
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical',
        classes=['VIRUS', 'NORMAL', 'BACTERIA']
    )

    model = tf.keras.models.Sequential([

        # 1
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 2
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 3
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 4
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2, 2),

        # 5
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2, 2),
        #tf.keras.layers.Dropout(0.3),

        # 6
        # tf.keras.layers.Conv2D(512, (3, 3), activation='relu'),
        # tf.keras.layers.MaxPooling2D(2, 2),
        # tf.keras.layers.Dropout(0.2),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    callback = tf.keras.callbacks.LearningRateScheduler(scheduler)
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(0.0001,momentum=0.9), metrics=['accuracy'])

    model.summary()

    # history = model.fit(
    #         train_data,
    #         #steps_per_epoch =54,
    #         epochs =40,
    #         validation_data = test_data,
    #         callbacks=callback
    #
    # )
    # model.save_weights('./checkpoints6/my_checkpoint6')

    model.load_weights('./checkpoints6/my_checkpoint6',)
    model.evaluate(new_test_data)

def scheduler(epoch, lr):
  if epoch < 13:
    return 0.0001
  if epoch < 25:
    return 0.00001
  if epoch < 40:
    return 0.000001



if __name__ == '__main__':
    CNN()