from flask import Flask
from flask import request
from flask_cors import CORS
import os
import base64
import tensorflow as tf
import json
import time

from pencil.pencil import pencil_draw, color_draw
from AnimeGAN.test import test_anime
from cartoon.test import test_main
from photo_resize import resize_600
from gaugan.test import doit
from gaugan.color_to_grey import *
from gaugan.get_from_nv import generate_result_from_nv, get_urls
from StegaStamp.md5_word_trans import save_word, resolve_md5

import sys


app = Flask(__name__)

cur_url_id = 0


def generate_dir_name():
    name = time.strftime('%Y-%m-%d', time.localtime())
    return name


def generate_file_name(str_date):
    name = str_date + ',' + str(time.time()).replace('.','-')
    return name


def makedirs_if_not_exist(str_dir):
    if not os.path.exists(str_dir):
        os.makedirs(str_dir) 


@app.route('/test', methods=['GET'])
def test():
    s_NORMAL = "0"
    s_DEBUG = "1"
    return s_DEBUG


@app.route('/pencil', methods=['POST'])
def pencil():
    img = request.values.get('img')
    color = request.values.get('color')
    gammaS = request.values.get('s')
    gammaI = request.values.get('i')
    quality = request.values.get('q')

    # print("img:"+str(img))
    img_input = base64.b64decode(img)

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)

    dir_input = 'pencil/userData/input/' + str_date + '/'
    pth_input = dir_input + str_time + '.jpg'
    dir_output = 'pencil/userData/output/' + str_date + '/'
    makedirs_if_not_exist(dir_input)
    makedirs_if_not_exist(dir_output)

    with open(pth_input, 'wb') as f:
        f.write(img_input)
    cmd = ['python ', ' --p ', ' --c ', ' -s ', ' -i ', ' -q ', ' -img ', ' --output_dir ']
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
        cmd_run = cmd[0] + pth_function + cmd[2] + cmd[3] + \
            gammaS + cmd[4] + gammaI + cmd[5] + quality + cmd[6] + pth_input + cmd[7] + dir_output
        pth_output = dir_output + str_time + '_color.jpg'
    else:
        # false for graphic pencil
        cmd_run = cmd[0] + pth_function + cmd[1] + cmd[3] + \
            gammaS + cmd[4] + gammaI + cmd[5] + quality + cmd[6] + pth_input + cmd[7] + dir_output
        pth_output = dir_output + str_time + '_pencil.jpg'

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


@app.route('/anime', methods=['POST'])
def anime():
    img = request.values.get('img')

    checkpoint_dir = 'AnimeGAN/checkpoint/'

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)

    dir_input = 'AnimeGAN/userData/input/' + str_date + '/' + str_time + '/'
    pth_input = dir_input + 'anime.jpg'
    dir_output = 'AnimeGAN/userData/output/' + str_date + '/' + str_time + '/'
    pth_output = dir_output + 'anime.jpg'
    makedirs_if_not_exist(dir_input)
    makedirs_if_not_exist(dir_output)

    if_adjust_brightness = True
    # source_dir = 'AnimeGAN/data/input/'
    # result_dir = 'AnimeGAN/data/output/'
    # source_pic_name = 'anime_input.jpg'

    img_input = base64.b64decode(img)
    with open(pth_input, 'wb') as f:
        f.write(img_input)

    resize_600(pth_input)

    test_anime(checkpoint_dir, dir_input, dir_output, if_adjust_brightness)

    with open(pth_output, 'rb') as f:
        img_output = f.read()
        img_output_base64 = base64.b64encode(img_output)

    return img_output_base64


@app.route('/oilpaint', methods=['POST'])
def oilpaint():
    # img - base64-encoded image
    # model - '0' for winter to summer
    # model - '1' for summer to winter
    img = request.values.get('img')
    model = request.values.get('model')

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)

    dir_input = 'oilpaint/userData/input/' + str_date + '/'
    pth_input = dir_input + str_time + '.jpg'
    dir_output = 'oilpaint/userData/output/' + str_date + '/'
    pth_output = dir_output + str_time + '.jpg'
    makedirs_if_not_exist(dir_input)
    makedirs_if_not_exist(dir_output)

    # input_path = 'oilpaint/data/input/input.jpg'
    # output_path = 'oilpaint/data/output/output.jpg'
    image_size = '256'

    img_ori = base64.b64decode(img)
    with open(pth_input, 'wb+') as f:
        f.write(img_ori)
    if model == '0':
        # winter2summer
        nm_model = 'oilpaint/models/winter2summer.pb'
    elif model == '1':
        nm_model = 'oilpaint/models/summer2winter.pb'
    else:
        return -1
    cmd = ['python', '--model', '--input', '--output', '--image_size']
    cmd_run = cmd[0] + ' ' + 'oilpaint/main.py' + ' ' + cmd[1] + ' ' + nm_model + ' ' + \
        cmd[2] + ' ' + pth_input + ' ' + cmd[3] + \
        ' ' + pth_output + ' ' + cmd[4] + image_size
    print(cmd_run)
    os.system(cmd_run)

    with open(pth_output, 'rb') as f:
        img_return = f.read()
        img_return_decode = base64.b64encode(img_return)

    return img_return_decode


@app.route('/cartoon', methods=['POST'])
def cartoon():
    img = request.values.get('img')

    source_dir = 'cartoon/images/input/'
    result_dir = 'cartoon/images/output/'
    source_pic_name = 'photo.jpg'

    img_input = base64.b64decode(img)
    with open(source_dir + source_pic_name, 'wb+') as f:
        f.write(img_input)

    status = test_main(source_dir + source_pic_name,
                       result_dir + source_pic_name)

    return_data = {}

    if status == 0:
        with open(result_dir + source_pic_name, 'rb') as f:
            img_output = f.read()
            img_output_base64 = base64.b64encode(img_output)
            return_data["status"] = status
            return_data["img"] = str(img_output_base64, encoding='utf-8')
        return json.dumps(return_data, ensure_ascii=False)
    else:
        # Can not detect face
        return_data["status"] = status
        return_data["img"] = ""
        return json.dumps(return_data, ensure_ascii=False)


@app.route('/paint', methods=['POST'])
def paint():
    img = request.values.get('img')

    source_dir = 'gaugan/images/input/'
    label_dir = source_dir + 'val_label/'
    color_label_dir = source_dir + 'color_label/'
    result_dir = 'gaugan/images/output/'
    source_pic_name = '1.png'
    greyscale_label_location = label_dir + source_pic_name
    restored_color_label_location = source_dir + \
        'restored_color_label/' + source_pic_name

    img_input = base64.b64decode(img)
    with open(color_label_dir + source_pic_name, 'wb+') as f:
        f.write(img_input)

    convert_rgb_image_to_greyscale(
        color_label_dir + source_pic_name, greyscale_label_location)
    restore_greyscale_to_rgb(greyscale_label_location,
                             restored_color_label_location)

    result_pic_location = 'gaugan/images/output/mv/result-%s.jpg' % str(time.time())

    global cur_url_id
    nv_urls = get_urls()
    max_tries = len(nv_urls)
    status_nv = 0
    while max_tries > 0:
        status_nv = generate_result_from_nv(restored_color_label_location, result_pic_location, nv_urls[cur_url_id])
        if(status_nv == 0):
            break;
        else:
            cur_url_id = (cur_url_id + 1) % len(nv_urls)
        max_tries = max_tries - 1
    
    if status_nv == 1:
        result_pic_location = 'gaugan/images/output/label2coco/test_latest/images/synthesized_image/1.png'
        args = ['--name', 'label2coco',
                '--checkpoints_dir', 'gaugan/checkpoints',
                '--load_size', '256',
                '--crop_size', '256',
                '--aspect_ratio', '1.0',
                '--preprocess_mode', 'resize_and_crop',
                '--dataset_mode', 'custom',
                '--gpu_ids', '-1',
                '--label_dir', source_dir + 'val_label',
                '--image_dir', source_dir + 'val_img',
                '--results_dir', result_dir,
                '--label_nc', '182',
                '--gpu_ids', '-1',
                '--no_instance',
                '--no_pairing_check']
        doit(args)
        print('generate finish')
    with open(result_pic_location, 'rb') as f:
        img_output = f.read()
        img_output_base64 = base64.b64encode(img_output)

    return img_output_base64


@app.route('/style_transfer', methods=['POST'])
def style_transfer():
    img = request.values.get('img')
    style_no = request.values.get('style_no')
    img_ori = base64.b64decode(img)

    print('style_no' + str(style_no))

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)

    dir_input = 'style_transfer/userData/input/' + str_date + '/'
    pth_input = dir_input + str_time + '.jpg'
    dir_output = 'style_transfer/userData/output/' + str_date + '/'
    pth_output = dir_output + str_time + '.jpg'
    makedirs_if_not_exist(dir_input)
    makedirs_if_not_exist(dir_output)

    # pth_input = 'style_transfer/in/content.jpg'
    # pth_output = 'style_transfer/out/output.jpg'

    with open(pth_input, 'wb+') as f:
        f.write(img_ori)

    cmd = 'cd style_transfer; /usr/bin/env /home/ubuntu/.conda/envs/style_transfer/bin/python main.py --style_no %s --path_content %s --path_output %s; cd ..' % (
        style_no, pth_input.split('style_transfer/')[1], pth_output.split('style_transfer/')[1])
    os.system(cmd)

    with open(pth_output, 'rb') as f:
        img_read = f.read()
        img_base64 = base64.b64encode(img_read)

    return img_base64


@app.route('/image_encry/encode', methods=['POST'])
def encode():
    img = request.values.get('img')
    txt = request.values.get('txt')
    
    img_ori = base64.b64decode(img)

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)
    dir_input = 'StegaStamp/userData/encode/upload/' + str_date + '/'
    pth_input = dir_input + str_time + '.png'
    dir_save = 'StegaStamp/userData/encode/save/' + str_date + '/' + str_time + '/'
    makedirs_if_not_exist(dir_input)
    makedirs_if_not_exist(dir_save)

    with open(pth_input, 'wb+') as f:
        f.write(img_ori)
    str_secret = save_word(txt)
    cmd = ['python', '--image', '--save_dir', '--secret']
    pth_repo = 'StegaStamp/'
    pth_ecd_function = pth_repo + 'encode_image.py'
    cmd_run = cmd[0] + ' ' + pth_ecd_function + ' ' + cmd[1] + ' ' + pth_input \
        + ' ' + cmd[2] + ' ' + dir_save + ' ' + \
        cmd[3] + ' ' + '\'' + str_secret + '\''
    print(cmd_run)
    os.system(cmd_run)  # launch image watermark model
    # to this step, encoded image is saved in ./save/decoded.png

    pth_encoded_img = dir_save + 'encoded.png'
    with open(pth_encoded_img, 'rb') as f:
        img_ecd = f.read()
        img_ecd_base64 = base64.b64encode(img_ecd)

    return img_ecd_base64


@app.route('/image_encry/decode', methods=['POST'])
def decode():
    img = request.values.get('img')
    img_ori = base64.b64decode(img)

    str_date = generate_dir_name()
    str_time = generate_file_name(str_date)
    dir_upload = 'StegaStamp/userData/decode/upload/' + str_date + '/'
    pth_upload = dir_upload + str_time + '.png'
    dir_save = 'StegaStamp/userData/decode/save/' + str_date + '/' + str_time + '/'
    makedirs_if_not_exist(dir_upload)
    makedirs_if_not_exist(dir_save)

    with open(pth_upload, 'wb+') as f:
        f.write(img_ori)
    cmd = ['python', '--image','--result_dir']
    pth_dcd_function = 'StegaStamp/decode_image.py'
    cmd_run = cmd[0] + ' ' + pth_dcd_function + ' ' + cmd[1] + ' ' + pth_upload + ' ' + cmd[2] + ' ' + dir_save
    print(cmd_run)
    os.system(cmd_run)
    pth_code = dir_save + 'code.txt'
    if not os.path.exists(pth_code):
        str_no_copyright_found = ''' {"author":"(图像中无版权信息)","date":"(空)","contact":"(空)","copyright":"(空)","area":"(空)"} '''
        return str_no_copyright_found
    with open(pth_code, 'r') as f:
        str_code = f.read()
    word = resolve_md5(str_code)
    return word


if __name__ == '__main__':
    f = open('server_log.log', 'a')
    # sys.stdout = f
    # sys.stderr = f
    with open('temp_cur_server_pid.tmp','w+') as f:
        f.write(str(os.getpid()))

    CORS(app, supports_credentials=True)
    app.run(
        host='0.0.0.0',
        port=8002,
        debug=True
    )
