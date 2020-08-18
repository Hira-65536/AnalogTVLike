# coding: utf-8
import sys
import numpy as np
from PIL import Image, ImageFilter,ImageChops,ImageDraw,ImageEnhance
import os,tkinter, tkinter.filedialog, tkinter.messagebox


TV_Like = 'n'

#setting.txtから読み取り
cnt=0
fname = 'setting.txt'
with open(fname,"r") as file:
    for i in file:
        if cnt == 0:
            TRANSMITTANCE=float(i.rstrip('\n'))
        elif cnt == 1:
            CONTRAST=float(i.rstrip('\n'))
        elif cnt == 2:
            BRIGHTNESS=float(i.rstrip('\n'))
        elif cnt == 3:
            GAUSSIAN=float(i.rstrip('\n'))
        elif cnt == 4:
            RED_THRESHOLD=float(i.rstrip('\n'))

        cnt+=1

#ノイズっぽい線を生成する。横列が偶数のとき、横線を描画してる
def AnalogLike_noise(img):
    draw_flag=False
    draw = ImageDraw.Draw(img)
    width,height = img.size
    for i in range(height):
        if draw_flag:
            draw.line(((0,i),(width,i)),int(TRANSMITTANCE),1)
        draw_flag = not draw_flag
    return img

#色収差を疑似的に作成したプログラム（改善の余地あり
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

            if r+int(RED_THRESHOLD)>255:
                r=254
            else:
                r+=int(RED_THRESHOLD)
            img.putpixel((x, y), (r, old_g, next_b, _))
            old_g=g

    return img

try:
    def main():
        # ファイル選択ダイアログの表示
        root = tkinter.Tk()
        root.withdraw()
        fTyp1 = [("", "*.png")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        image_data = tkinter.filedialog.askopenfilename(filetypes=fTyp1,initialdir=iDir)
        print('AnalogTVLike-Converter START')
        #image_data=input('plz image pass:')
        #ファイルを正しく選択した場合、処理を行う。そうでない場合は終了。
        if os.path.isfile(image_data):
            print(image_data)
            title=image_data[:-4]
            input_img = Image.open(image_data)
        else:
            print('this image not exist.')
            sys.exit()
        #画像が大きすぎるとき、リサイズする
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
        new_gray_img.putalpha(int(TRANSMITTANCE))
        #合成（乗算）
        mix_img=ImageChops.multiply(input_img, new_gray_img)

        Analoglike_img = Color_setting(mix_img)
        Analoglike_img.putalpha(int(TRANSMITTANCE))
        new_mix_img = ImageChops.multiply(input_img, Analoglike_img)
        # コントラスト処理
        enhancer = ImageEnhance.Contrast(new_mix_img)
        enhance_image = enhancer.enhance(CONTRAST)
        # 明るさ処理
        enhancer = ImageEnhance.Brightness(Analoglike_img)
        enhance_image = enhancer.enhance(BRIGHTNESS)
        enhance_image.putalpha(255)
        # ぼかし処理
        enhance_image.filter(ImageFilter.GaussianBlur(GAUSSIAN))
        #TV_Like=input('add frame?[y/N]') or 'n'
        # フレームの有無
        TV_Like=tkinter.messagebox.askquestion('showquestion', 'フレームを追加しますか？')
        if TV_Like=='yes':
            frame = Image.open('sample/frame.png')
            frame_resize=frame.resize(enhance_image.size)
            frame_resize = frame_resize.convert('RGBA')
            enhance_image.paste(frame_resize,(0,0),frame_resize.split()[3])
            out_frame = ('_frame_')
        else:
            out_frame =('_')
        result_img = enhance_image
        result_img.show()
        if 'yes'==tkinter.messagebox.askquestion('showquestion', 'これで保存しますか？'):
            result_img.save(title+out_frame+'output.png')
            print('output success!!')
        else:
            print('output failed!!')

    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    pass

finally:
    sys.exit
