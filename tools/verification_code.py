# -*- coding: utf8 -*-

from PIL import Image
import pytesseract


# 去除噪点
def clear_noise(img):  # img：图片地址
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    # img = Image.open('/home/yang/png/0.png') # 读入图片
    pixdata = img.load()
    X = img.size[0] - 1  # 因为我校的验证码二值化后正好剩下一圈宽度为一像素的白边，所以这么处理了
    Y = img.size[1] - 1

    def icolor(RGBA):
        if RGBA == white: return (1)
        else:
            return (0)

    for y in range(Y):
        for x in range(X):
            if (x < 1 or y < 1):
                pass
            else:
                if icolor(pixdata[x, y]) == 1:
                    pass
                else:
                    if (icolor(pixdata[x + 1, y]) + icolor(pixdata[x, y + 1]) +
                            icolor(pixdata[x - 1, y]) +
                            icolor(pixdata[x, y - 1]) +
                            icolor(pixdata[x - 1, y - 1]) +
                            icolor(pixdata[x + 1, y - 1]) +
                            icolor(pixdata[x - 1, y + 1]) +
                            icolor(pixdata[x + 1, y + 1])) > 6:
                        # 如果一个黑色像素周围的8个像素中白色像素数量大于5个，则判断其为噪点，填充为白色
                        pixdata[x, y] = white
                        # 填充白点
    for y in range(Y):
        for x in range(X):
            if (x < 1 or y < 1):
                pass
            else:
                if icolor(pixdata[x, y]) == 0:
                    pass
                else:
                    if ((icolor(pixdata[x + 1, y])) +
                        (icolor(pixdata[x, y + 1])) +
                        (icolor(pixdata[x - 1, y])) +
                        (icolor(pixdata[x, y - 1]))) < 2:
                        # 如果一个白色像素上下左右4个像素中黑色像素的个数大于2个，则判定其为有效像素，填充为黑色。
                        pixdata[x, y] = black
    # 二次去除黑点
    for y in range(Y):
        for x in range(X):
            if (x < 1 or y < 1):
                pass
            else:
                if icolor(pixdata[x, y]) == 1:
                    pass
                else:
                    if (icolor(pixdata[x + 1, y]) + icolor(pixdata[x, y + 1]) +
                            icolor(pixdata[x - 1, y]) +
                            icolor(pixdata[x, y - 1])) > 2:
                        pixdata[x, y] = white
    # img.show()
    return img


def two(img):  # img：图片地址
    i = 0
    # img = Image.open('/home/yang/png/0.png') # 读入图片
    img = img.convert("RGBA")
    while i < 4:  # 循环次数视情况进行调整
        i = i + 1
        pixdata = img.load()
        # 一次二值化

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:  # 使RGB值中R小于90的像素点变成纯黑
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 190:  # 使RGB值中G小于90的像素点变成纯黑
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:  # 使RGB值中B大于0的像素点变成纯白
                    pixdata[x, y] = (255, 255, 255, 255)

    # 理论上的二值化代码只有上面那些，RGB值的调整阈值需要针对不同验证码反复调整。同时实际中一组阈值往往没法做到完美，后面的部分是视实际情况添加的类似部分

    # 二次二值化（除去某些R、G、B值接近255的颜色）
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 254:
                pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 254:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

    # 三次二值化，怼掉纯黄色（实际使用中发现很多图片最后剩几个纯黄色的像素点）
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 0, 255):
                pixdata[x, y] = (0, 0, 0, 255)

    # img.show()
    return img


def del_noise(im):
    #   去除边框的黑色
    data = im.getdata()
    w, h = im.size
    black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x < 2 or y < 2:
                im.putpixel((x - 1, y - 1), (255, 255, 255))
            if x > w - 3 or y > h - 3:
                im.putpixel((x + 1, y + 1), (255, 255, 255))
    # im.show()
    print('图像降噪完成')
    # image.save('xxxx.jpg')
    return im


if __name__ == '__main__':
    # path = '/home/zg/Downloads/work/code-num.jpeg'
    path = '/home/zg/Downloads/work/code.png'
    image = Image.open(path)
    image = two(image)
    # image.show()
    # image = clear_noise(image)
    #
    # image.show()
    # image = del_noise(image)
    # image.show()

    result = pytesseract.image_to_string(image)
    print(result)