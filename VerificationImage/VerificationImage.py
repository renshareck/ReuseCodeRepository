# -*- coding:utf-8 -*-
import random
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class VerificationImage:

    def __init__(self, length):
        self.length = length
        self.threshold = 30 # 相似度阈值
        self.font_size = 36 # 字体大小
        self.obstruct_line = 2 # 干扰线数目

        self.single_width = int(1.25 * self.font_size)
        self.single_height = int(1.25 * self.font_size)

        self.width = int(0.75 * self.font_size * length)
        self.height = int(1.4 * self.font_size)

        #字体库
        self.font_list = ["arial.ttf", "Gabriola.ttf", "Inkfree.ttf", "segoesc.ttf"]

        #随机字符库
        self.random_char_list = []
        for i in range(0, 10):
            self.random_char_list.append(str(i))
        for i in range(97, 123):# 小写字母
            self.random_char_list.append(chr(i))
        for i in range(65, 91):# 大写字母
            self.random_char_list.append(chr(i))
        #去除             "0"     "I"       "O"       "i"     "l"         "o"
        similar_list = [str(0), chr(73), chr(79), chr(105), chr(108), chr(111)]
        for similar_char in similar_list:
            self.random_char_list.remove(similar_char)

    #rgb转hsv
    @staticmethod
    def hsv(R, G, B):
        r = R/255.0
        g = G/255.0
        b = B/255.0
        H = 0
        S = 0
        V = 0
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        detal = cmax - cmin

        if (detal == 0):
            H = 0
        elif (cmax == r):
            H = 60 * (((g - b)/detal) % 6)
        elif (cmax == g):
            H = 60 * (((b - r)/detal) + 2)
        elif (cmax == b):
            H = 60 * (((r - g)/detal) + 4)

        if (cmax == 0):
            S = 0
        else:
            S = detal*1.0/cmax

        V = cmax
        return(H, S, V)

    #计算hsv空间相似度
    @staticmethod
    def cal_similar(R1, G1, B1, R2, G2, B2):
        r = 10
        h = 10

        H1, S1, V1 = VerificationImage.hsv(R1, G1, B1)
        H2, S2, V2 = VerificationImage.hsv(R2, G2, B2)

        x1 = r * V1 * S1 * math.cos(H1 / 180.0 * math.pi)
        y1 = r * V1 * S1 * math.sin(H1 / 180.0 * math.pi)
        z1 = h * (1 - V1)

        x2 = r * V2 * S2 * math.cos(H1 / 180.0 * math.pi)
        y2 = r * V2 * S2 * math.sin(H1 / 180.0 * math.pi)
        z2 = h * (1 - V2)

        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2

        similar = dx*dx + dy*dy + dz*dz
        return similar

    #计算相似度测试代码
    @staticmethod
    def test_cal_similar():
        img = Image.new(mode="RGB", size=(255, 1024), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        for i in range(0, 256):
            draw.line((0, i * 4, 255, i * 4), fill=(i, 255, 255), width=4)
            print(VerificationImage.cal_similar(0, 255, 255, i, 255, 255), i)
        with open("cal_similar.png", "wb") as f:
            img.save(f, format="png")
        #测试决定当 similar < 30 是断定为相似颜色

    # 生成随机颜色
    def getRandomColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    #生成随机字符
    def getRandomChar(self):
        random_char = random.choice(self.random_char_list)
        return random_char

    #生成字图片
    def RootImgGenerate(self, R, G, B):
        #RGB为验证码背景颜色
        # 创建一张透明背景的图片
        img = Image.new(mode="RGBA", size=(self.single_width, self.single_height), color=0)

        # 获取图片画笔，用于描绘字
        draw = ImageDraw.Draw(img)

        # 修改字体
        font = ImageFont.truetype(font=random.choice(self.font_list), size=self.font_size)
        # 随机生成5种字符+5种颜色
        random_txt = self.getRandomChar()
        txt_color = self.getRandomColor()
        while(self.cal_similar(txt_color[0], txt_color[1], txt_color[2], R, G, B) < self.threshold):
            txt_color = self.getRandomColor()
        draw.text((int(0.25 * self.font_size), 0), text=random_txt, fill=txt_color, font=font)

        #放缩
        img = img.resize((int(self.single_width * random.randint(90, 110) / 100), int(self.single_height * random.randint(90, 110) / 100)))

        #旋转
        img = img.rotate(random.randint(-15, 15))

        return img
        # 打开图片操作，并保存在当前文件夹下
        #with open("test.png",  "wb") as f:
        #    img_rotate.save(f, format="png")


    def createImg(self):
        # 创建一张随机背景色的图片
        #bg_color = self.getRandomColor()
        bg_color = (255, 255, 255)
        img = Image.new(mode="RGBA", size=(self.width, self.height), color=bg_color)

        for i in range(self.length):
            single_img = self.RootImgGenerate(bg_color[0], bg_color[1], bg_color[2])
            single_r, single_g, signle_b, single_a = single_img.split()
            img.paste(single_img, (int(0.7 * self.font_size) * i, 0), single_a)

        draw = ImageDraw.Draw(img)
        for i in range(self.obstruct_line):
            x1 = random.randint(0, int(self.width / 6))
            x2 = random.randint(int(5 * self.width / 6), self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.getRandomColor())

        # 打开图片操作，并保存在当前文件夹下
        with open("test.png",  "wb") as f:
            img.save(f, format="png")

if __name__ == "__main__":
    test = VerificationImage(5)
    test.createImg()
    #test.RootImgGenerate(255, 255, 255)
    #VerificationImage.test_cal_similar()