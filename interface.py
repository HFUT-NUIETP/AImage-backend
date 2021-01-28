from flask import Flask
from flask import request
from flask_cors import CORS
import os
import base64
import tensorflow as tf

from pencil.pencil import pencil_draw,color_draw
from AnimeGAN.test import test_anime

app = Flask(__name__)
#CORS(app, resources=r'/*')

@app.route('/pencil', methods = ['POST'])
def pencil():
    img = request.values.get('img')
    color = request.values.get('color')
    gammaS = request.values.get('s')
    gammaI = request.values.get('i')
    quality = request.values.get('q')
    img_input = base64.b64decode(img)
    with open('pencil/input/input.jpg', 'wb') as f:
        f.write(img_input)
    cmd = ['python ',' --p ', ' --c ', ' -s ', ' -i ', ' -q ']
    # cmd----[0]------ [1]------[2]-----[3]------[4]-----[5]
    '''
    --p for graphic
    --c for color
    --s for gammaS param
    --i for gammaI param
    '''
    pth_function = 'pencil/draw.py'
    if (color == 'True'):
        # true for colorful pencil
        cmd_run = cmd[0] + pth_function + cmd[2] + cmd[3] + gammaS + cmd[4] + gammaI + cmd[5] + quality
        pth_output = 'pencil/output/input_color.jpg'
    else:
        # false for graphic pencil
        cmd_run = cmd[0] + pth_function + cmd[1] + cmd[3] + gammaS + cmd[4] + gammaI + cmd[5] + quality
        pth_output = 'pencil/output/input_pencil.jpg'
    
    print("------------Debug--------------")
    print(color)
    print(cmd_run)
    os.system(cmd_run)
	
    with open(pth_output, 'rb') as f:
        img_output = f.read()
        img_output_base64 = base64.b64encode(img_output)

    # print(img_output_base64)
    print("------------Debug--------------")
    return img_output_base64

@app.route('/test', methods=['GET'])
def test():
    return 'hello_3'

@app.route('/anime', methods=['POST'])
def anime():
    img = request.values.get('img')

    checkpoint_dir = 'AnimeGAN/checkpoint/'
    source_dir = 'AnimeGAN/data/input/'
    result_dir = 'AnimeGAN/data/output/'
    if_adjust_brightness = True
    source_pic_name = 'anime_input.jpg'

    img_input = base64.b64decode(img)
    with open(source_dir + source_pic_name, 'wb') as f:
        f.write(img_input)
    
    test_anime(checkpoint_dir, source_dir, result_dir, if_adjust_brightness)

    with open(result_dir + source_pic_name, 'rb') as f:
        img_output = f.read()
        img_output_base64 = base64.b64encode(img_output)

    return img_output_base64

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(
            host = '0.0.0.0',
            port = 8002,  
            debug = True 
            )

