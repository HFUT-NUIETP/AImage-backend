import tensorflow as tf
import os

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('model', 'models/winter2summer.pb', 'model path (.pb)')
tf.flags.DEFINE_string('input', 'input/input.jpg', 'input image path (.jpg)')
tf.flags.DEFINE_string('output', 'output/output.jpg', 'output image path (.jpg)')
tf.flags.DEFINE_integer('image_size', '256', 'image size, default: 256')

def convert2float(image):
  """ Transfrom from int image ([0,255]) to float tensor ([-1.,1.])
  """
  image = tf.image.convert_image_dtype(image, dtype=tf.float32)
  return (image/127.5) - 1.0

def inference():
  graph = tf.Graph()

  with graph.as_default():
    with tf.gfile.FastGFile(FLAGS.input, 'rb') as f:
      image_data = f.read()
      input_image = tf.image.decode_jpeg(image_data, channels=3)
      input_image = tf.image.resize_images(input_image, size=(FLAGS.image_size, FLAGS.image_size))
      input_image = convert2float(input_image)
      input_image.set_shape([FLAGS.image_size, FLAGS.image_size, 3])

    with tf.gfile.FastGFile(FLAGS.model, 'rb') as model_file:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(model_file.read())
    [output_image] = tf.import_graph_def(graph_def,
                          input_map={'input_image': input_image},
                          return_elements=['output_image:0'],
                          name='output')

  with tf.Session(graph=graph) as sess:
    generated = output_image.eval()
    with open(FLAGS.output, 'wb+') as f:
      f.write(generated)

def main(unused_argv):
  inference()

if __name__ == '__main__':
  tf.app.run()
