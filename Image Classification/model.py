from __future__ import absolute_import, division, print_function
import os
import json
import pickle
import logging
import numpy as np
import tensorflow as tf
import multiprocessing as md
from datetime import datetime as dt

tf.enable_eager_execution()

# Re-organize all image file paths 
# and corresponding labels into a tuple of lists
def data_lists(data_dir, label_mapping):
    files = os.listdir(data_dir)
    file_ids = [f.split('.')[0] for f in files]
    filepaths = [os.path.join(data_dir, f) for f in files]
    mapping_file = open(label_mapping, 'r')
    mapping_json = json.load(mapping_file)
    labels = [int(mapping_json[id]) for id in file_ids]
    return (filepaths, labels)

# Set up a generator for normalize images and encoded labels (one hot)
def data_fn(filepaths, labels, batch_size, repeat_count, categories, training):
    files = tf.constant(filepaths)
    labels = tf.constant(labels)
    dataset = tf.data.Dataset.from_tensor_slices((files, labels))
    if training:
        dataset = dataset.shuffle(len(filepaths))
    dataset = dataset.repeat(count=repeat_count)
    def parse_function(file, label):
        # Read and decode PNG files
        image_string = tf.read_file(file)
        image = tf.image.decode_png(image_string, channels=3)
        # Rescale pixel values between [0, 1]
        image = tf.image.convert_image_dtype(image, tf.float32)
        # Normalize images
        image = tf.image.per_image_standardization(image)
        # Encode label as one hot vectors
        label = tf.one_hot(label, categories)
        return image, label
    dataset = dataset.map(parse_function, num_parallel_calls=md.cpu_count())
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(1)
    return dataset.make_one_shot_iterator()

# Identity block in the network
def model_unit(filters, kernel_size, initializer):
    def get_inputs(inputs):
        # Bottleneck layer to reduce the parameter number 
        outputs = tf.keras.layers.Conv2D(filters // 2, 1, 1, 'same', use_bias=False, kernel_initializer=initializer)(inputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = tf.keras.layers.Conv2D(filters, kernel_size, 1, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = tf.keras.layers.Conv2D(filters // 2, 1, 1, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = tf.keras.layers.Conv2D(filters, kernel_size, 1, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.Add()([outputs, inputs])
        outputs = tf.keras.layers.ELU()(outputs)
        return outputs
    return get_inputs

# The whole model
def model_fn(initializer):
    def classify(categories):
        inputs = tf.keras.Input(shape=(254, 254, 3))
        outputs = tf.keras.layers.Conv2D(64, 3, 2, 'same', use_bias=False, kernel_initializer=initializer)(inputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = model_unit(64, 3, initializer=initializer)(outputs)
        outputs = tf.keras.layers.Conv2D(128, 3, 2, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = model_unit(128, 3, initializer=initializer)(outputs)
        outputs = tf.keras.layers.Conv2D(256, 3, 2, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = model_unit(256, 3, initializer=initializer)(outputs)
        outputs = tf.keras.layers.Conv2D(512, 3, 2, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = model_unit(512, 3, initializer=initializer)(outputs)
        outputs = tf.keras.layers.Conv2D(1024, 3, 2, 'same', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        # Get output size from the previous layer
        out_size = tf.keras.backend.int_shape(outputs)
        k = out_size[1]
        # Conv layer with 1-by-1 output to replace huge FC layer
        outputs = tf.keras.layers.Conv2D(2048, k, 1, 'valid', use_bias=False, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.BatchNormalization()(outputs)
        outputs = tf.keras.layers.ELU()(outputs)
        outputs = tf.keras.layers.Flatten()(outputs)
        outputs = tf.keras.layers.Dense(categories, kernel_initializer=initializer)(outputs)
        outputs = tf.keras.layers.Softmax()(outputs)
        return tf.keras.Model(inputs=inputs, outputs=outputs)
    return classify

def loss(model, inputs, labels):
    predictions = model(inputs)
    return tf.losses.softmax_cross_entropy(labels, predictions)

def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, model.variables)

def save_model_weights(model, model_dir=None, filename=None):
    if not model_dir:
        model_dir = './'
    if not filename:
        filename = 'mw.' + str(dt.now().timestamp()) + '.pkl'
    filepath = os.path.join(model_dir, filename)
    model_params = model.get_weights()
    model_weights_file = open(filepath, 'wb')
    pickle.dump(model_params, model_weights_file)
    model_weights_file.close()

def restore_model_weights(model, weights_filepath):
    weights_file = open(weights_filepath, 'rb')
    weights = pickle.load(weights_file, encoding='utf8')
    model.set_weights(weights)
    weights_file.close()

def train(data_gen, optimizer, model, model_dir, save_step=100):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    for (i, (x, y)) in enumerate(data_gen):
        loss_value = loss(model, x, y)
        grads = grad(model, x, y)
        optimizer.apply_gradients(zip(grads, model.variables))
        step_info = 'time->{0},batch->{1:d},loss->{2:f}'.format(dt.now(), i + 1, loss_value.numpy())
        print(step_info)
        logging.info(step_info)
        if (i + 1) % save_step == 0:
            save_model_weights(model, model_dir)
    save_model_weights(model, model_dir)

# Compute correct classifications in batches
def validate(data_gen, model):
    count = 0
    for (x, y) in data_gen:
        predictions = model(x)
        max_per_line = tf.reduce_max(predictions, axis=[1], keepdims=True)
        res = tf.multiply(tf.round(tf.div(predictions, max_per_line)), y)
        count += tf.reduce_sum(res).numpy()
    return count

def main(training):
    if training:
        logfile_name = 'training.' + str(dt.now().timestamp()) + '.log'
        logging.basicConfig(filename=logfile_name, level=logging.INFO)

        m_dir = './model/'
        existing_mw = './model/mw.pkl'
        inputs, labels = data_lists('./training/', './img_pos.json')
        categories = 48
        batch_size = 32
        epochs = 2
        lr = 1e-3
        save_steps = 400

        data_iter = data_fn(inputs, labels, batch_size, epochs, 48, True)
        optimizer = tf.train.AdamOptimizer(learning_rate=lr)
        model = model_fn(initializer='he_normal')(categories)
        if os.path.exists(existing_mw):
            restore_model_weights(model, existing_mw)
        train(data_iter, optimizer, model, m_dir, save_step=save_steps)
    else:
        existing_mw = './model/mw.pkl'
        inputs, labels = data_lists('./testing/', './img_pos.json')
        categories = 48
        batch_size = 32
        data_iter = data_fn(inputs, labels, batch_size, 1, 48, False)
        model = model_fn(initializer='he_normal')(categories)
        restore_model_weights(model, existing_mw)
        acc = validate(data_iter, model) / len(inputs)
        print(acc)

if __name__ == '__main__':
    main(training=False)