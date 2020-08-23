# coding: utf-8
import sys
import numpy as np
from PIL import Image, ImageFilter,ImageChops,ImageDraw,ImageEnhance,ImageSequence
import os,tkinter, tkinter.filedialog, tkinter.messagebox


TV_Like = 'n'
GIF_FLAG = False
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

def AnalogLike_noise(img):
    draw_flag=False
    draw = ImageDraw.Draw(img)
    width,height = img.size
    for i in range(height):
        if draw_flag:
            draw.line(((0,i),(width,i)),int(TRANSMITTANCE),1)
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

            if r+int(RED_THRESHOLD)>255:
                r=254
            else:
                r+=int(RED_THRESHOLD)
            img.putpixel((x, y), (r, old_g, next_b, _))
            old_g=g

    return img

def get_frames(path):
    '''パスで指定されたファイルのフレーム一覧を取得する
    '''
    im = Image.open(path)
    return (frame.copy() for frame in ImageSequence.Iterator(im))



try:
    def img_convert(input_img):
        input_img = input_img.convert('RGBA')
        gray_img = input_img.convert('L')
        # ノイズの追加
        noise_img = AnalogLike_noise(gray_img)
        # 透明化のためにRGBAに変換
        new_gray_img = noise_img.convert('RGBA')
        # グレースケールを透過
        new_gray_img.putalpha(int(TRANSMITTANCE))
        # 合成（乗算）
        mix_img = ImageChops.multiply(input_img, new_gray_img)

        Analoglike_img = Color_setting(mix_img)
        Analoglike_img.putalpha(int(TRANSMITTANCE))
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
        enhance_image.filter(ImageFilter.GaussianBlur(GAUSSIAN))
        return enhance_image

    def main():
        count=0
        result_img=[]
        # ファイル選択ダイアログの表示
        root = tkinter.Tk()
        root.withdraw()
        fTyp1 = [("", "*.*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        image_data = tkinter.filedialog.askopenfilename(filetypes=fTyp1,initialdir=iDir)
        print('AnalogTVLike-Converter START')
        #image_data=input('plz image pass:')
        format_img=image_data[-3:]
        if format_img=='png' or format_img=='jpg':
            GIF_FLAG=False
        elif format_img=='gif':
            GIF_FLAG=True
        else:
            tkinter.messagebox.showerror('確認', '画像ファイルを選択してください。')
            sys.exit()
        if os.path.isfile(image_data) and os.path.isfile('sample/frame.png'):
            print(image_data)
            title=image_data[:-4]
            frames = get_frames(image_data)
        else:
            print('this image not exist.')
            tkinter.messagebox.showerror('確認', '加工画像またはフレームがみつかりません。\nフレーム画像（frame.png）は、sampleという名前のディレクトリに入れてください。')
            sys.exit()
        TV_Like = tkinter.messagebox.askquestion('showquestion', 'フレームを追加しますか？')
        for input_img in frames:
            x,y=input_img.size
            if x>1920 and y>1080:
                x=1920
                y=1080
                input_img=input_img.resize((x,y))
                print('resize image')
            enhance_image=img_convert(input_img)
            #TV_Like=input('add frame?[y/N]') or 'n'
            if TV_Like=='yes':
                frame = Image.open('sample/frame.png')
                frame_resize=frame.resize(enhance_image.size)
                frame_resize = frame_resize.convert('RGBA')
                enhance_image.paste(frame_resize,(0,0),frame_resize.split()[3])
                out_frame = ('_frame_')
            else:
                out_frame =('_')
            result_img.append(enhance_image)
            count+=1
            print(str(count)+'枚目の処理終了')

        #result_img.show()
        if GIF_FLAG:
            tkinter.messagebox.showinfo('確認', 'GIFアニメの確認画面はないため、保存後にご自身でご確認お願いします。')
        else:
            result_img[0].show()
        if 'yes'==tkinter.messagebox.askquestion('showquestion', '保存しますか？'):
            if GIF_FLAG:
                result_img[0].save(title+out_frame+'output.gif',save_all=True, append_images=result_img[1:],duration=100,loop=0)
            else:
                result_img[0].save(title + out_frame + 'output.' + format_img)
            tkinter.messagebox.showinfo('確認','保存に成功しました。')
            print('output success!!')
        else:
            tkinter.messagebox.showerror('確認', '保存に失敗しました。')
            print('output failed!!')

    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    pass

finally:
    sys.exit