import os
from pencil.pencil import pencil_draw,color_draw

def pencil(color, s, i):
    gammaS = s
    gammaI = i
    cmd = ['python ',' --p ', ' --c ', ' -s ', ' -i ']
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
    print(cmd_run)
    os.system(cmd_run)
	
    pth_output = 'pencil/output/output.jpg'
    ## output 2 base64 encoded format
    # with open(pth_output, 'rb') as f:
    #     img_output = f.read()
    #     img_output_base64 = base64.b64encode(img_output)
    # os.system('rm input/* -r')
    # os.system('rm output/* -r')


if __name__ == '__main__':
    pencil(True, '1', '1')