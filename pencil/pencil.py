#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import numpy as np
from scipy import signal
from scipy.ndimage import interpolation
from scipy.sparse import csr_matrix as csr_matrix, spdiags as spdiags
from scipy.sparse.linalg import spsolve as spsolve
import math
import cv2
import os
import sys


basedir = os.path.dirname(__file__)
output = os.path.join(basedir, 'output')

line_len_divisor = 40   # 卷积核大小与图片的倍数关系
# gammaS = 1      # 值越大, 轮廓的线条越粗
# gammaI = 1      # 值越大, 最后输出图片的颜色越深

Lambda = 0.2
texture_resize_ratio = 0.2
texture_file_name = 'pencil/texture.jpg'

def pencil_draw(path="pencil/input/input.jpg", gammaS=1, gammaI=1):
    name = path.rsplit("/")[-1].split(".")[0]
    suffix = path.rsplit("/")[-1].split(".")[1]

    imr = Image.open(path)
    type = "colour" if imr.mode == "RGB" else "black"
    im = imr.convert("L")
    J = np.array(im)
    S = get_s(J, gammaS=gammaS)
    T = get_t(J, type, gammaI=gammaI)
    IPencil = S * T
    img = Image.fromarray(IPencil * 255)
    # img.show()

    ## save image
    # save_output(Image.fromarray(S * 255), name + "_s", suffix)
    # save_output(Image.fromarray(T * 255), name + "_t", suffix)
    save_output(img, name + "_pencil", suffix)

    return name + suffix

def color_draw(path="pencil/input/input.jpg", gammaS=1, gammaI=1):
    im = Image.open(path)

    if im.mode == 'RGB':
        ycbcr = im.convert('YCbCr')
        Iruv = np.ndarray((im.size[1], im.size[0], 3), 'u1', ycbcr.tobytes())
        type = "colour"
    else:
        Iruv = np.array(im)
        type = "black"

    S = get_s(Iruv[:, :, 0], gammaS=gammaS)
    T = get_t(Iruv[:, :, 0], type, gammaI=gammaI)
    Ypencil = S * T

    new_Iruv = Iruv.copy()
    new_Iruv.flags.writeable = True
    new_Iruv[:, :, 0] = Ypencil * 255

    R = cv2.cvtColor(new_Iruv, cv2.COLOR_YCR_CB2BGR)
    img = Image.fromarray(R)

    name = path.rsplit("/")[-1].split(".")[0]
    suffix = path.rsplit("/")[-1].split(".")[1]

    # save_output(Image.fromarray(S * 255), name + "_s", suffix)
    # save_output(Image.fromarray(T * 255), name + "_t", suffix)
    save_output(img, name + "_color", suffix)

# ---------------------------------------
# -----------------utils-----------------
# ---------------------------------------

'''
stitch begin
'''
def hstitch(I, width):
    Istitched = I
    while Istitched.shape[1] < width:
        window_size = int(round(I.shape[1] / 4))
        left = I[:, (I.shape[1] - window_size) : I.shape[1]]
        right = I[:, 0:window_size]
        aleft = np.zeros((left.shape[0], window_size))
        aright = np.zeros((left.shape[0], window_size))
        for i in range(window_size):
            aleft[:, i] = left[:, i] * (1 - float(i+1)/window_size)
            aright[:, i] = right[:, i] * float(i+1)/window_size
        Istitched = np.column_stack(
            (Istitched[:, 0:(Istitched.shape[1] - window_size)],
             aleft + aright,
             Istitched[:, window_size: Istitched.shape[1]])
        )
    Istitched = Istitched[:, 0:width]
    return Istitched


def vstitch(I, height):
    Istitched = I
    while Istitched.shape[0] < height:
        window_size = int(round(I.shape[0] / float(4)))
        up = I[(I.shape[0] - window_size):I.shape[0], :]
        down = I[0:window_size, :]
        aup = np.zeros((window_size, up.shape[1]))
        adown = np.zeros((window_size, up.shape[1]))
        for i in range(window_size):
            aup[i, :] = up[i, :] * (1 - float(i+1)/window_size)
            adown[i, :] = down[i, :] * float(i+1)/window_size
        Istitched = np.row_stack(
            (Istitched[0: Istitched.shape[0] - window_size, :],
             aup + adown,
             Istitched[window_size: Istitched.shape[0], :])
        )
    Istitched = Istitched[0: height, :]
    return Istitched
'''
stitch end
'''

'''
util begin
'''
def im2double(I):
    Min = I.min()
    Max = I.max()
    dis = float(Max - Min)
    m, n = I.shape
    J = np.zeros((m, n), dtype="float")
    for x in range(m):
        for y in range(n):
            a = I[x, y]
            if a != 255 and a != 0:
                b = float((I[x, y] - Min) / dis)
                J[x, y] = b
            J[x, y] = float((I[x, y] - Min) / dis)
    return J


def rot90(I, n=1):
    rI = I
    for x in range(n):
        # rI = zip(*rI[::-1])
        rI = list(zip(*rI[::-1]))
    return rI


def rot90c(I):
    rI = I
    for x in range(3):
        rI = rot90(rI)
    return rI

'''
util end
'''

'''
natural histogram matching begin
'''
def heaviside(x):
    return x if x >= 0 else 0


def p1(x):
    return float(1) / 9 * math.exp(-(256 - x) / float(9)) * heaviside(256 - x)


def p2(x):
    return float(1) / (225 - 105) * (heaviside(x - 105) - heaviside(x - 225))


def p3(x):
    return float(1) / math.sqrt(2 * math.pi * 11) * \
           math.exp(-((x - 90) ** 2) / float(2*(11 ** 2)))


def p(x, type="black"):
    if type == "colour":
        return 62*p1(x) + 30*p2(x) + 5*p3(x)
    else:
        return 76*p1(x) + 22*p2(x) + 2*p3(x)


def natural_histogram_matching(I, type="black"):
    ho = np.zeros((1, 256))
    po = np.zeros((1, 256))
    for i in range(256):
        po[0, i] = sum(sum(1 * (I == i)))     # d
    po /= float(sum(sum(po)))
    ho[0, 0] = po[0, 0]
    for i in range(1, 256):
        ho[0, i] = ho[0, i-1] + po[0, i]
    histo = np.zeros((1, 256))
    prob = np.zeros((1, 256))
    for i in range(256):
        # prob[0, i] = p(i+1) # eq.4
        prob[0, i] = p(i, type) # eq.4
    prob /= float(sum(sum(prob)))
    histo[0] = prob[0]
    for i in range(1, 256):
        histo[0, i] = histo[0, i-1] + prob[0, i]
    Iadjusted = np.zeros((I.shape[0], I.shape[1]))
    for x in range(I.shape[0]):
        for y in range((I.shape[1])):
            histogram_value = ho[0, I[x, y]]
            index = (abs(histo - histogram_value)).argmin()
            Iadjusted[x, y] = index
    Iadjusted /= float(255)
    return Iadjusted

'''
natural histogram matching end
'''
def get_s(J, gammaS=1):    
    h, w = J.shape
    line_len_double = float(min(h, w)) / line_len_divisor
    line_len = int(line_len_double)
    line_len += line_len % 2
    half_line_len = line_len / 2
    dJ = im2double(J)
    Ix = np.column_stack((abs(dJ[:, 0:-1] - dJ[:, 1:]), np.zeros((h, 1))))
    Iy = np.row_stack((abs(dJ[0:-1, :] - dJ[1:, :]), np.zeros((1, w))))
    Imag = np.sqrt(Ix*Ix + Iy*Iy)
    L = np.zeros((line_len, line_len, 8))
    for n in range(8):
        if n == 0 or n == 1 or n == 2 or n == 7:
            for x in range(0, line_len):
                y = round(((x+1) - half_line_len) * math.tan(math.pi/8*n))
                y = half_line_len - y
                if 0 < y <= line_len:
                    L[int(y-1), x, n] = 1
                if n < 7:
                    L[:, :, n+4] = rot90c(L[:, :, n])
    L[:, :, 3] = rot90(L[:, :, 7])

    G = np.zeros((J.shape[0], J.shape[1], 8))
    for n in range(8):
        G[:, :, n] = signal.convolve2d(Imag, L[:, :, n], "same")    # eq.2

    Gindex = G.argmax(axis=2)   # 获取最大值元素所在的下标 axis表示维度
    # C is map set
    C = np.zeros((J.shape[0], J.shape[1], 8))
    for n in range(8):
        C[:, :, n] = Imag * (1 * (Gindex == n))
    Spn = np.zeros((J.shape[0], J.shape[1], 8))
    for n in range(8):
        Spn[:, :, n] = signal.convolve2d(C[:, :, n], L[:, :, n], "same")
    Sp = Spn.sum(axis=2)
    Sp = (Sp - Sp[:].min()) / (Sp[:].max() - Sp[:].min())
    S = (1 - Sp) ** gammaS
    img = Image.fromarray(S * 255)

    return S


def get_t(J, type, gammaI=1):
    Jadjusted = natural_histogram_matching(J, type=type) ** gammaI

    texture = Image.open(texture_file_name)
    texture = np.array(texture.convert("L"))
    texture = texture[99: texture.shape[0]-100, 99: texture.shape[1]-100]

    ratio = texture_resize_ratio * min(J.shape[0], J.shape[1]) / float(1024)
    texture_resize = interpolation.zoom(texture, (ratio, ratio))
    texture = im2double(texture_resize)
    htexture = hstitch(texture, J.shape[1])
    Jtexture = vstitch(htexture, J.shape[0])

# --------------ori-----------------
    # size = J.shape[0] * J.shape[1]

    # nzmax = 2 * (size-1)
    # i = np.zeros((nzmax, 1))
    # j = np.zeros((nzmax, 1))
    # s = np.zeros((nzmax, 1))
    # for m in range(1, nzmax+1):
    #     i[m-1] = int(math.ceil((m+0.1) / 2)) - 1
    #     j[m-1] = int(math.ceil((m-0.1) / 2)) - 1
    #     s[m-1] = -2 * (m % 2) + 1
    # dx = csr_matrix((s.T[0], (i.T[0], j.T[0])), shape=(size, size))

    # nzmax = 2 * (size - J.shape[1])
    # i = np.zeros((nzmax, 1))
    # j = np.zeros((nzmax, 1))
    # s = np.zeros((nzmax, 1))
    # for m in range(1, nzmax+1):
    #     i[m-1, :] = int(math.ceil((m-1+0.1)/2) + J.shape[1] * (m % 2)) - 1
    #     j[m-1, :] = math.ceil((m-0.1)/2) - 1
    #     s[m-1, :] = -2 * (m % 2) + 1
    # dy = csr_matrix((s.T[0], (i.T[0], j.T[0])), shape=(size, size))
    # Jtexture1d = np.log(np.reshape(Jtexture.T, (1, Jtexture.size), order="f") + 0.01)
    # Jtsparse = spdiags(Jtexture1d, 0, size, size)
    # Jadjusted1d = np.log(np.reshape(Jadjusted.T, (1, Jadjusted.size), order="f").T + 0.01)

    # nat = Jtsparse.T.dot(Jadjusted1d)   # lnJ(x)
    # a = np.dot(Jtsparse.T, Jtsparse)
    # b = dx.T.dot(dx)
    # c = dy.T.dot(dy)
    # mat = a + Lambda * (b + c)     # lnH(x)
    # beta1d = spsolve(mat, nat)  # eq.8
    # beta = np.reshape(beta1d, (J.shape[0], J.shape[1]), order="c")
# --------------ori end-----------------

# ---------------fast-------------------

    hei, wid = J.shape
    # fx = np.array([1, -1])
    fx = np.array([[1], [-1]])
    fy = np.array([[1], [-1]])
    otfFx = psf2otf(fx, [hei, wid])
    otfFy = psf2otf(fy, [hei, wid])
    DxDy = abs(otfFx)**2 + abs(otfFy)**2
    LnH = np.log(Jtexture+0.0001)
    LnJ = np.log(Jadjusted+0.0001)
    Nom =  np.fft.fft2(LnJ / LnH)
    Denom = 1 + gammaI * DxDy
    # beta1d = np.fft.ifft2(Nom / Denom)
    beta1d_real = np.fft.ifft2(Nom / Denom)
    beta1d = np.real(beta1d_real)
    beta = beta1d
# --------------fast end----------------

    T = Jtexture ** beta    # eq.9
    T = (T - T.min()) / (T.max() - T.min())
    img = Image.fromarray(T * 255)

    return T


# # -------------fast utils---------------
def zero_pad(image, shape, position='corner'):
    shape = np.asarray(shape, dtype=int)
    imshape = np.asarray(image.shape, dtype=int)
    if np.alltrue(imshape == shape):
        return image
    if np.any(shape <= 0):
        raise ValueError("ZERO_PAD: null or negative shape given")
    dshape = shape - imshape
    if np.any(dshape < 0):
        raise ValueError("ZERO_PAD: target size smaller than source one")
    pad_img = np.zeros(shape, dtype=image.dtype)
    idx, idy = np.indices(imshape)
    if position == 'center':
        if np.any(dshape % 2 != 0):
            raise ValueError("ZERO_PAD: source and target shapes "
                             "have different parity.")
        offx, offy = dshape // 2
    else:
        offx, offy = (0, 0)
    pad_img[idx + offx, idy + offy] = image
    return pad_img

def psf2otf(psf, shape):
    if np.all(psf == 0):
        return np.zeros_like(psf)
    inshape = psf.shape
    psf = zero_pad(psf, shape, position='corner')
    for axis, axis_size in enumerate(inshape):
        psf = np.roll(psf, -int(axis_size / 2), axis=axis)
    otf = np.fft.fft2(psf)
    n_ops = np.sum(psf.size * np.log2(psf.shape))
    otf = np.real_if_close(otf, tol=n_ops)

    return otf
# #-----------fast utils end--------------

def make_output_dir():
    if not os.path.exists(output):
        os.mkdir(output)


def save_output(img, name, suffix):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    make_output_dir()
    name = os.path.join(output, name)
    filename = "{0}.{1}".format(name, suffix)
    img.save(filename)
