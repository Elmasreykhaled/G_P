# Importing library
import numpy as np
import tensorflow as tf
from keras.models import load_model


def get_result(img_path, model_path):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224, 3))
    img = tf.keras.utils.img_to_array(img) / 255
    img = np.array([img])
    img.shape
    model = load_model(model_path)
    prediction = model.predict(img)
    result = np.argmax(prediction)
    return result




