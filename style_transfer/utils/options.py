import argparse
import os


class StyleOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--path_content', type=str, default='in/content.jpg', help='input content image path')
        self.parser.add_argument('--path_styles', type=str, default='utils/styles/style',
                                 help='input style image path')
        self.parser.add_argument('--style_no', type=int, default=0, help='style no, 0-25')
        self.parser.add_argument('--path_output', type=str, default='out/output.jpg', help='output result path')
        self.parser.add_argument('--size_content', type=int, default=384, help='width and height of content input')
        self.parser.add_argument('--size_style', type=int, default=256, help='width and height of style input')
        self.parser.add_argument('--path_style_prd', type=str, default='utils/models/predict_256_int8.tflite',
                                 help='style prediction model path')
        self.parser.add_argument('--path_style_trans', type=str, default='utils/models/transform_256_int8.tflite',
                                 help='style transform model path')
        self.config = self.parser.parse_args()


if __name__ == '__main__':
    config = StyleOptions().config
    os.system('python options.py -h')
    print(config)
