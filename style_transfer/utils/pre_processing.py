import tensorflow as tf
from PIL import Image
import numpy as np


# Function to load an image from a file, and add a batch dimension.
def load_img(path):
    img = tf.io.read_file(path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]

    return img


# Function to pre-process by resizing an central cropping it.
def resize_image(image, size):
    # Resize the image so that the shorter dimension becomes 256px.
    shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = size / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    image = tf.image.resize(image, new_shape)

    # Central crop the image.
    image = tf.image.resize_with_crop_or_pad(image, size, size)

    return image


def stylized_array_im_reshape(im_array):
    return im_array.squeeze(axis=0)


def ndarray2image(im_array):
    return Image.fromarray(np.uint8(im_array*255.0))


def imsave_from_image(im, path):
    im.save(path)


def imsave_from_array(im_array, path):
    im = ndarray2image(im_array)
    imsave_from_image(im, path)

