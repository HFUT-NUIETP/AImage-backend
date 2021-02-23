from utils.pre_processing import *
from utils.style import *


def test(config):
    im_content = resize_image(load_img(config.path_content), config.size_content)
    im_style = resize_image(load_img(config.path_styles+str(config.style_no)+'.jpg'), config.size_style)

    style_bottleneck = style_predict(im_style, config=config)

    im_stylized = style_transform(style_bottleneck, im_content, config)

    return im_stylized


def test_and_save(config):
    im_stylized = test(config)
    im_stylized = stylized_array_im_reshape(im_stylized)
    imsave_from_array(im_stylized, config.path_output)


if __name__ == '__main__':
    pass
    # config = StyleOptions().config
    # im_stylized = test(config=config)

