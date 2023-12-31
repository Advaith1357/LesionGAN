# -*- coding: utf-8 -*-
"""FINAL - NTCopy of Data Augmentation Classifier

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OFSssMAKu7IHlLn8hv4X1Cr1QOysiR09
"""

from google.colab import drive
drive.mount('/content/drive')

PATH = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/Vanilla-NT/'
val_path = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/Vanilla-NT-Holdout'

import tensorflow as tf
def create_model(base_model, num_classes):
    x=base_model.output
    x=GlobalAveragePooling2D()(x)
    x=tf.keras.layers.Dense(100,activation='relu', kernel_initializer=tf.keras.initializers.VarianceScaling(), use_bias=True)(x)
    preds=tf.keras.layers.Dense(num_classes,activation='softmax', kernel_initializer=tf.keras.initializers.VarianceScaling(), use_bias=False)(x)

    model=Model(inputs=base_model.input,outputs=preds)
    return model

from tensorflow.keras.optimizers import Adam, Adadelta, Adagrad, Adamax, Ftrl, Nadam, RMSprop, SGD
def get_optimizer(optimizer_name, learning_rate):

    print('Selected Optimizer', optimizer_name)
    switcher = {
        'Adadelta': Adadelta(learning_rate=learning_rate),
        'Adagrad': Adagrad(learning_rate=learning_rate),
        'Adam': Adam(learning_rate=learning_rate),
        'Adamax': Adamax(learning_rate=learning_rate),
        'FTRL': Ftrl(learning_rate=learning_rate),
        'NAdam': Nadam(learning_rate=learning_rate),
        'RMSprop': RMSprop(learning_rate=learning_rate),
        'Gradient Descent': SGD(learning_rate=learning_rate)
    }
    return switcher.get(optimizer_name, Adam(learning_rate=learning_rate))

import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from keras.applications.resnet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,GlobalAveragePooling2D
from keras.models import Model
from tensorflow.keras import regularizers
from tensorflow.keras.preprocessing import image_dataset_from_directory
from keras.callbacks import EarlyStopping
from tensorflow import keras

epochs = 50
base_learning_rate = 0.0001
optimizer = 'Adam'
BATCH_SIZE = 32
num_classes = 8
IMG_SIZE = (224, 224)

train_datagen_preprocessed = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator_preprocessed = train_datagen_preprocessed.flow_from_directory(PATH,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=True)
validation_generator_preprocessed = train_datagen_preprocessed.flow_from_directory(val_path,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=False)


base_model_preprocessed = tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', alpha=0.35)
for layer in base_model_preprocessed.layers:
    layer.trainable=False
model = create_model(base_model_preprocessed,num_classes)
model.compile(optimizer = get_optimizer(optimizer_name=optimizer,learning_rate=base_learning_rate),loss='CategoricalCrossentropy',metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
early_stopping_monitor = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=30,
    verbose=0,
    mode='auto',
    baseline=None,
    restore_best_weights=True
)
step_size_train = train_generator_preprocessed.n//train_generator_preprocessed.batch_size
history_fine_preprocessed = model.fit(train_generator_preprocessed,
                        epochs=epochs,
                        callbacks=[early_stopping_monitor],
                        validation_data = validation_generator_preprocessed,
                        verbose=1)

# Import numpy for calculating best model accuracy
import numpy as np
# Populating matrics -> accuracy & loss
prc_p = history_fine_preprocessed.history['val_precision']
rec_p = history_fine_preprocessed.history['val_recall']
acc_p = history_fine_preprocessed.history['val_accuracy']
loss_p = history_fine_preprocessed.history['val_loss']

def seperate_labels(generator):
    x_validation = []
    y_validation = []
    num_seen = 0

    for x, labels in generator:
        x_validation.append(x)
        y_validation.append([argmax(label) for label in labels])
        num_seen += len(x)
        if num_seen == generator.n: break

    x_validation = np.concatenate(x_validation)
    y_validation = np.concatenate(y_validation)
    return x_validation, y_validation

# Calculate and display the confusion matrix
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import argmax
from sklearn.metrics import ConfusionMatrixDisplay

x_validation, y_validation = seperate_labels(validation_generator_preprocessed)
y_pred = model.predict(x_validation, batch_size=BATCH_SIZE)
predictions = np.apply_along_axis(argmax, 1, y_pred)
display_labels = validation_generator_preprocessed.class_indices.keys()

ConfusionMatrixDisplay.from_predictions(y_validation, predictions, display_labels=display_labels, cmap="binary")
plt.show()

accuracy_with_original_dataset =acc_p
loss_with_original_dataset = loss_p
precision_with_original_dataset =prc_p
recall_with_original_dataset = rec_p

PATH = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/GAN_Plus_Vanilla90/'
val_path = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/Vanilla-NT-Holdout'

epochs = 50
base_learning_rate = 0.0001
optimizer = 'Adam'
BATCH_SIZE = 32
num_classes = 8
IMG_SIZE = (224, 224)

train_datagen_GAN = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator_GAN = train_datagen_GAN.flow_from_directory(PATH,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=True)
validation_generator_GAN = train_datagen_GAN.flow_from_directory(val_path,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=False)


base_model_GAN = tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', alpha=0.35)
for layer in base_model_GAN.layers:
    layer.trainable=False
model = create_model(base_model_GAN,num_classes)
model.compile(optimizer = get_optimizer(optimizer_name=optimizer,learning_rate=base_learning_rate),loss='CategoricalCrossentropy',metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
early_stopping_monitor = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=30,
    verbose=0,
    mode='auto',
    baseline=None,
    restore_best_weights=True
)
step_size_train = train_generator_GAN.n//train_generator_GAN.batch_size
history_fine_GAN = model.fit(train_generator_GAN,
                        epochs=epochs,
                        callbacks=[early_stopping_monitor],
                        validation_data = validation_generator_GAN,
                        verbose=1)

x_validation, y_validation = seperate_labels(validation_generator_GAN)
y_pred = model.predict(x_validation, batch_size=BATCH_SIZE)
predictions = np.apply_along_axis(argmax, 1, y_pred)
display_labels = validation_generator_GAN.class_indices.keys()

ConfusionMatrixDisplay.from_predictions(y_validation, predictions, display_labels=display_labels, cmap="binary")
plt.show()

prc_g = history_fine_GAN.history['val_precision_1']
rec_g = history_fine_GAN.history['val_recall_1']
acc_g = history_fine_GAN.history['val_accuracy']
loss_g = history_fine_GAN.history['val_loss']

accuracy_with_GAN_augmented_dataset = acc_g
loss_with_GAN_augmented_dataset =  loss_g
precision_with_GAN_augmented_dataset =  prc_g
recall_with_GAN_augmented_dataset =  rec_g

PATH = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/DA_Plus_Vanilla90/'
val_path = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/Vanilla-NT-Holdout'

epochs = 50
base_learning_rate = 0.0001
optimizer = 'Adam'
BATCH_SIZE = 32
num_classes = 8
IMG_SIZE = (224, 224)

train_datagen_DA = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator_DA = train_datagen_DA.flow_from_directory(PATH,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=True)
validation_generator_DA = train_datagen_DA.flow_from_directory(val_path,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=False)


base_model_DA = tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', alpha=0.35)
for layer in base_model_DA.layers:
    layer.trainable=False
model = create_model(base_model_DA,num_classes)
model.compile(optimizer = get_optimizer(optimizer_name=optimizer,learning_rate=base_learning_rate),loss='CategoricalCrossentropy',metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
early_stopping_monitor = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=30,
    verbose=0,
    mode='auto',
    baseline=None,
    restore_best_weights=True
)
step_size_train = train_generator_DA.n//train_generator_DA.batch_size
history_fine_DA = model.fit(train_generator_DA,
                        epochs=epochs,
                        callbacks=[early_stopping_monitor],
                        validation_data = validation_generator_DA,
                        verbose=1)

x_validation, y_validation = seperate_labels(validation_generator_DA)
y_pred = model.predict(x_validation, batch_size=BATCH_SIZE)
predictions = np.apply_along_axis(argmax, 1, y_pred)
display_labels = validation_generator_DA.class_indices.keys()

ConfusionMatrixDisplay.from_predictions(y_validation, predictions, display_labels=display_labels, cmap="binary")
plt.show()

prc_d = history_fine_DA.history['val_precision_2']
rec_d = history_fine_DA.history['val_recall_2']
acc_d = history_fine_DA.history['val_accuracy']
loss_d = history_fine_DA.history['val_loss']

accuracy_with_augmented_dataset =acc_d
loss_with_augmented_dataset = loss_d
precision_with_augmented_dataset =prc_d
recall_with_augmented_dataset = rec_d

PATH = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/GAN_Plus_DA_Plus_Vanilla90/'
val_path = '/content/drive/Shareddrives/1:1 Advaith Menon/Downloads/final_datasets/Vanilla-NT-Holdout'

epochs = 50
base_learning_rate = 0.0001
optimizer = 'Adam'
BATCH_SIZE = 32
num_classes = 8
IMG_SIZE = (224, 224)

train_datagen_combined = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator_combined = train_datagen_combined.flow_from_directory(PATH,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=True)
validation_generator_combined = train_datagen_combined.flow_from_directory(val_path,
                                                target_size=IMG_SIZE,
                                                color_mode='rgb',
                                                batch_size=BATCH_SIZE,
                                                class_mode='categorical',
                                                shuffle=False)


base_model_combined = tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', alpha=0.35)
for layer in base_model_combined.layers:
    layer.trainable=False
model = create_model(base_model_combined,num_classes)
model.compile(optimizer = get_optimizer(optimizer_name=optimizer,learning_rate=base_learning_rate),loss='CategoricalCrossentropy',metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
early_stopping_monitor = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=30,
    verbose=0,
    mode='auto',
    baseline=None,
    restore_best_weights=True
)
step_size_train = train_generator_combined.n//train_generator_combined.batch_size
history_fine_combined = model.fit(train_generator_combined,
                        epochs=epochs,
                        callbacks=[early_stopping_monitor],
                        validation_data = validation_generator_combined,
                        verbose=1)

x_validation, y_validation = seperate_labels(validation_generator_combined)
y_pred = model.predict(x_validation, batch_size=BATCH_SIZE)
predictions = np.apply_along_axis(argmax, 1, y_pred)
display_labels = validation_generator_combined.class_indices.keys()

ConfusionMatrixDisplay.from_predictions(y_validation, predictions, display_labels=display_labels, cmap="binary")
plt.show()

prc_c = history_fine_combined.history['val_precision_3']
rec_c = history_fine_combined.history['val_recall_3']
acc_c = history_fine_combined.history['val_accuracy']
loss_c = history_fine_combined.history['val_loss']

accuracy_with_combined_dataset = acc_c
loss_with_combined_dataset =  loss_c
precision_with_combined_dataset =  prc_c
recall_with_combined_dataset =  rec_c

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.plot(np.arange(50), accuracy_with_original_dataset, color='green',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), accuracy_with_augmented_dataset, color='red',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), accuracy_with_GAN_augmented_dataset, color='blue',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), accuracy_with_combined_dataset, color='purple',
     linewidth=2, markersize=12)

plt.xlabel("Epoch Count")
plt.ylabel("Accuracy")

plt.show()

plt.plot(np.arange(50), loss_with_original_dataset, color='green',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), loss_with_augmented_dataset, color='red',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), loss_with_GAN_augmented_dataset, color='blue',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), loss_with_combined_dataset, color='purple',
     linewidth=2, markersize=12)

plt.xlabel("Epoch Count")
plt.ylabel("Loss")

plt.show()

plt.plot(np.arange(50), recall_with_original_dataset, color='green',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), recall_with_augmented_dataset, color='red',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), recall_with_GAN_augmented_dataset, color='blue',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), recall_with_combined_dataset, color='purple',
     linewidth=2, markersize=12)

plt.xlabel("Epoch Count")
plt.ylabel("Recall")
plt.show()

plt.plot(np.arange(50), precision_with_original_dataset, color='green',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), precision_with_augmented_dataset, color='red',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), precision_with_GAN_augmented_dataset, color='blue',
     linewidth=2, markersize=12)
plt.plot(np.arange(50), precision_with_combined_dataset, color='purple',
     linewidth=2, markersize=12)

plt.xlabel("Epoch Count")
plt.ylabel("Precision")

plt.show()