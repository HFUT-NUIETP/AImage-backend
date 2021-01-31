from PIL import Image


def resize_600(path):
    # 长或宽超过600则按照比例缩小
    imr = Image.open(path)
    width = imr.size[0]
    height = imr.size[1]

    if (width > height and width > 600):
        rate = 600 / width
        imr = imr.resize((int(width * rate), int(height * rate)),Image.ANTIALIAS)
        print('Photo has been resized')
    elif (height >= width and height > 600):
        rate = 600 / height
        imr = imr.resize((int(width * rate), int(height * rate)),Image.ANTIALIAS)
        print('Photo has been resized')
    imr.save(path)
    return imr


if __name__ == '__main__':
    path = 'output.jpg'
    imr = resize_600(path)
    print('test')
    