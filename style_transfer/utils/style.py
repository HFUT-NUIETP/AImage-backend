import tensorflow as tf


def style_predict(style_image, config):
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=config.path_style_prd)

    # Set model input.
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], style_image)

    # Calculate style bottleneck.
    interpreter.invoke()
    style_bottleneck = interpreter.tensor(interpreter.get_output_details()[0]["index"])()

    return style_bottleneck


def style_transform(style_bottleneck, content_image, config):
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=config.path_style_trans)

    # Set model input.
    input_details = interpreter.get_input_details()
    interpreter.allocate_tensors()

    # Set model inputs.
    interpreter.set_tensor(input_details[0]["index"], content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()

    # Transform content image.
    stylized_image = interpreter.tensor(interpreter.get_output_details()[0]["index"])()

    return stylized_image
