from flask import Flask
from flask import request
from flask_cors import CORS
import os
import base64

from pencil.pencil import pencil_draw,color_draw

app = Flask(__name__)

@app.route('/pencil', methods = ['POST'])
def pencil():
    img = request.values.get('img')
    color = request.values.get('color')
    gammaS = request.values.get('s')
    gammaI = request.valules.get('i')
    img_input = base64.b64decode(img)
    with open('pencil/input/input.jpg', 'wb') as f:
        f.write(img_input)
    cmd = ['python ',' --p ', ' --c ', '-s ', '-i ']
    # cmd----[0]------ [1]------[2]-----[3]----[4]
    '''
    --p for graphic
    --c for color
    --s for gammaS param
    --i for gammaI param
    '''
    pth_function = 'pencil/draw.py'
    if (color == True):
        # true for colorful pencil
        cmd_run = cmd[0] + pth_function + cmd[2] + cmd[3] + gammaS + cmd[4] + gammaI
    else:
        # false for graphic pencil
        cmd_run = cmd[0] + pth_function + cmd[1] + cmd[3] + gammaS + cmd[4] + gammaI
    
    os.system(cmd_run)
	
    pth_output = 'pencil/output/output.jpg'
    with open(pth_output, 'rb') as f:
        img_output = f.read()
        img_output_base64 = base64.b64encode(img_output)
    os.system('rm input/* -r')
    os.system('rm output/* -r')

    return img_output_base64

@app.route('/test', methods=['GET'])
def test():
    return 'hello'

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(
            host = '0.0.0.0',
            port = 8001,  
            debug = True 
            )
