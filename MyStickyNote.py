import ctypes
from PIL import Image, ImageDraw, ImageFont
import winreg
import win32event
import os
import win32process


def edit_notepad(textpath=None):
    if textpath is None:
        dir_path = os.path.split(os.path.realpath(__file__))[0]
        textpath = os.path.join(dir_path, 'default.txt')
        textpath = ' ' + textpath
    handle = win32process.CreateProcess('c:\\windows\\notepad.exe', textpath, None, None, 0,
                                        win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())

    win32event.WaitForSingleObject(handle[0], -1)


def set_img_as_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\Desktop", access=winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "WallPaper", 0, winreg.REG_SZ, filepath)


def draw_text(textpath="default.txt"):
    lines = open(textpath).readlines()
    layer_0 = Image.open(lines[0][:-1]).convert('RGBA')

    layer_1 = Image.new('RGBA', layer_0.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer_1)
    head_fnt = ImageFont.truetype("ariblk.ttf", 40)
    text_fnt = ImageFont.truetype("Deng.ttf", 18)
    rec_x_left = int(layer_0.size[0] / 4 * 3)
    rec_y_left = 0
    text_x = int(layer_0.size[0] / 4 * 3) + 50

    draw.rectangle((rec_x_left, rec_y_left, *layer_0.size), fill=(0, 0, 0, 128))
    text_y = int(layer_0.size[1] / 13 * 1)
    draw.text((text_x, text_y), "DON'T FORGET", font=head_fnt, fill=(255, 255, 255, 255))

    lines = open(textpath).readlines()
    lines_len = min(len(lines), 11)
    for i in range(1, lines_len):
        text_y = int(layer_0.size[1] / 13 * (i + 1))
        draw.text((text_x, text_y), lines[i], font=text_fnt, fill=(255, 255, 255, 255))

    out = Image.alpha_composite(layer_0, layer_1)
    out.save('mystickNote.png')


if __name__ == '__main__':
    edit_notepad()
    draw_text("default.txt")
    dir_path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(dir_path, 'mystickNote.png')
    print(path)
    set_img_as_wallpaper(path)

