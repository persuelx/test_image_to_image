import tkinter
import tkinter as tk
from tkinter import Button, Canvas, Entry, Frame, Scrollbar
from tkinter import Tk, Frame, Menu, Toplevel, X
from tkinter.filedialog import *
import tkinter.messagebox
from tkinter.tix import Control
from PIL import Image, ImageTk
import cv2
class DataAnnotationWindow(object):
    def __init__(self):
        self.img_Wid = 1000
        self.img_Hei = 1000
        self.win_wid = self.img_Wid + 200
        self.win_Hei = self.img_Hei
        # init state control variable
        self.has_select_path = False  # sign has select image path(to do data annotation) or not
        self.src_img_path = ""
        self.dst_img_path = ""
        self.result_w = ""
        self.result_H = ""
        self.img_list = []
       # create main window
        self.mainWin = tkinter.Tk()
        self.mainWin.geometry(str(self.win_wid) + 'x' + str(self.win_Hei))  # init the size of window
        self.mainWin.title("data annotation tool")
        self.mainWin.tk.eval('package require Tix')
        # create init image(a black background)
        self.img = Image.new("RGB", (self.img_Wid, self.img_Hei), (0, 0, 0))
        self.photo_img = ImageTk.PhotoImage(self.img)
        # create Canvas control
        self.cv = Canvas(self.mainWin, bg='white', width=self.img_Wid, height=self.img_Hei)
        self.cv.create_image((0, 0), anchor=tkinter.NW, image=self.photo_img)
        self.cv.pack(side=tkinter.LEFT, expand=True)
        # create total Frame to lay out all components
        self.frame = Frame(self.mainWin)
        self.frame.pack(fill=tkinter.X, expand=tkinter.YES, side=tkinter.LEFT)
        # create text control
        root_save_path = './'
        self.entry = Entry(self.frame, state='normal')
        self.entry.pack(side=tkinter.TOP, fill=tkinter.X)
        self.entry.insert(0, root_save_path)
        # mkdir of annotation result
        self.categoryList = ['Dog', 'Cat']
        self.category_savepath_list = []
        for category in self.categoryList:
            cur_category_save_path = os.path.join(root_save_path, category)
            self.category_savepath_list.append(cur_category_save_path)
            if os.path.exists(cur_category_save_path) == False:
                os.mkdir(cur_category_save_path)
        # create 'START' button
        self.btn_start = Button(self.frame, text='select1', command=self._selectPath, activeforeground='blue',
                                activebackground='white', bg='blue', fg='white')
        self.btn_start.pack(side=tkinter.TOP, pady=30)

        # create data annotation label button
        self.btn_dog = Button(self.frame, text='select2', command=self._selectPath2,
                              activeforeground='black',
                              activebackground='blue', bg='white', fg='black')
        self.btn_dog.pack(side=tkinter.TOP, pady=10)

        self.textExample = tk.Text(self.frame, height=2)  # 文本输入框
        self.textExample.pack(side=tkinter.TOP, pady=15)  # 把Text放在window上面，显示Text这个控件
        self.textExample2 = tk.Text(self.frame, height=2)  # 文本输入框
        self.textExample2.pack(side=tkinter.TOP, pady=20)  # 把Text放在window上面，显示Text这个控件

        self.btn_get = Button(self.frame, text='获取参数', command=self.getTextInput, activeforeground='blue',
                               activebackground='white', bg='red', fg='white')
        self.btn_get.pack(side=tkinter.TOP, pady=10)

        self.btn_execute = Button(self.frame, text='执行', command=self.execut, activeforeground='blue',
                               activebackground='white', bg='red', fg='white')
        self.btn_execute.pack(side=tkinter.TOP, pady=10)
        # create 'QUIT' button
        self.btn_quit = Button(self.frame, text='QUIT', command=self.mainWin.quit, activeforeground='blue',
                               activebackground='white', bg='red', fg='white')
        self.btn_quit.pack(side=tkinter.BOTTOM, pady=10)
    def get_entry_value(self, entry1, entry2):
        self.input_path = entry1.get()
        self.output_path = entry2.get()
    def getTextInput(self):
        self.result_w = self.textExample.get("1.0", "end")  # 获取文本框输入的内容
        self.result_h = self.textExample2.get("1.0", "end")  # 获取文本框输入的内容
        print("self.result_w ======== ",self.result_w)
        print("self.result_H ======== ", self.result_h)
    def _selectPath2(self):
        # self.img_path = tkinter.filedialog.askdirectory()
        self.dst_img_path = tkinter.filedialog.askopenfilename()
        # self.img = Image.open(self.src_img_path).resize((self.img_Wid, self.img_Hei))
        # self.photo_img = ImageTk.PhotoImage(self.img)
        # self.cv.create_image((0, 0), anchor=tkinter.NW, image=self.photo_img)
    def _selectPath(self):
        # self.img_path = tkinter.filedialog.askdirectory()
        self.src_img_path = tkinter.filedialog.askopenfilename()
        # self.img = Image.open(self.src_img_path).resize((self.img_Wid, self.img_Hei))
        # self.photo_img = ImageTk.PhotoImage(self.img)
        # self.cv.create_image((0, 0), anchor=tkinter.NW, image=self.photo_img)
    def execut(self):
        """
        :param mother_img: 母图
        :param son_img: 子图
        :param save_img: 保存图片名
        :param coordinate: 子图在母图的坐标
        :return:
        """
        # 将图片赋值,方便后面的代码调用
        M_Img = Image.open(self.src_img_path)
        S_Img = Image.open(self.dst_img_path)
        factor = 1  # 子图缩小的倍数1代表不变，2就代表原来的一半
        # 给图片指定色彩显示格式
        M_Img = M_Img.convert("RGBA")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）
        # 获取图片的尺寸
        M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
        print("母图尺寸：", M_Img.size)
        S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
        print("子图尺寸：", S_Img.size)
        size_w = int(S_Img_w / float(self.result_w))
        size_h = int(S_Img_h / float(self.result_h))
        # 防止子图尺寸大于母图
        if S_Img_w > size_w:
            S_Img_w = size_w
        if S_Img_h > size_h:
            S_Img_h = size_h
        # # 重新设置子图的尺寸
        # icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
        icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
        w = int((M_Img_w - S_Img_w) / 2)
        h = int((M_Img_h - S_Img_h) / 2)
        coordinate = (350, 350)
        try:
            if coordinate == None or coordinate == "":
                coordinate = (w, h)
                # 粘贴子图到母图的指定坐标（当前居中）
                M_Img.paste(icon, coordinate, mask=None)
            else:
                print("已经指定坐标")
                # 粘贴子图到母图的指定坐标（当前居中）
                M_Img.paste(icon, coordinate, mask=None)
        except:
            print("坐标指定出错 ")
        # 保存图片
        self.img = M_Img.resize((self.img_Wid, self.img_Hei))
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.cv.create_image((0, 0), anchor=tkinter.NW, image=self.photo_img)
        # M_Img.save(save_img)

if __name__ == '__main__':
    data_annotation_tool = DataAnnotationWindow()
    tkinter.mainloop()  # run GUI