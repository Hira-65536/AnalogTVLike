# coding: utf-8
import sys
import numpy as np
from PIL import Image, ImageFilter,ImageChops,ImageDraw,ImageEnhance
import os

TRANSMITTANCE = int(255*0.6)
CONTRAST = 0.8
BRIGHTNESS = 1.3
RED_THRESHOLD = 15
TV_Like = 'n'

def AnalogLike_noise(img):
    draw_flag=False
    draw = ImageDraw.Draw(img)
    width,height = img.size
    for i in range(height):
        if draw_flag:
            draw.line(((0,i),(width,i)),TRANSMITTANCE,1)
        draw_flag = not draw_flag
    return img

def Color_setting(img):
    width,height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b , _= img.getpixel((x, y))
            if width-2>=x:
                _r, _g, next_b, __ = img.getpixel((x+1, y))
            else:
                next_b=b
            if y==0 and x==0:old_g=g

            if not r+RED_THRESHOLD>255:
                r+=RED_THRESHOLD
            img.putpixel((x, y), (r, old_g, next_b, _))
            old_g=g

    return img
    #return  img
try:
    def main():
        print('AnalogTVLike-Converter')
        image_data=input('plz image pass:')
        if os.path.isfile(image_data):
            input_img = Image.open(image_data)
        else:
            print('this image not exist.')
            sys.exit()
        x,y=input_img.size
        if x>1920 and y>1080:
            x=1920
            y=1080
            input_img=input_img.resize((x,y))
            print('resize image')

        input_img = input_img.convert('RGBA')
        gray_img = input_img.convert('L')
        #ノイズの追加
        noise_img=AnalogLike_noise(gray_img)
        #透明化のためにRGBAに変換
        new_gray_img = noise_img.convert('RGBA')
        #グレースケールを透過
        new_gray_img.putalpha(TRANSMITTANCE)
        #合成（乗算）
        mix_img=ImageChops.multiply(input_img, new_gray_img)

        Analoglike_img = Color_setting(mix_img)
        Analoglike_img.putalpha(TRANSMITTANCE)
        new_mix_img = ImageChops.multiply(input_img, Analoglike_img)
        # enhancerオブジェクト生成
        enhancer = ImageEnhance.Contrast(new_mix_img)
        # enhancerオブジェクトの強調
        enhance_image = enhancer.enhance(CONTRAST)
        # enhancerオブジェクト生成
        enhancer = ImageEnhance.Brightness(Analoglike_img)
        # enhancerオブジェクトの強調
        enhance_image = enhancer.enhance(BRIGHTNESS)
        enhance_image.putalpha(255)
        TV_Like=input('add frame?[y/N]') or 'n'
        if TV_Like=='y' or TV_Like=='Y':
            frame = Image.open('C:/cv_img/tmp/frame.png')
            frame_resize=frame.resize(enhance_image.size)
            frame_resize = frame_resize.convert('RGBA')
            enhance_image.paste(frame_resize,(0,0),frame_resize.split()[3])
            title = ('frame_')
        else:
            title=('no_frame_')
        result_img = enhance_image
        result_img.show()
        result_img.save(title+'output.png')
        print('output success!!')

    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    pass

finally:
    sys.exit