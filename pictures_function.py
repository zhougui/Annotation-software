from ui.canvas_function import CanvasFunction
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class PicturesFunction(CanvasFunction):
    def __init__(self, parent):
        super(PicturesFunction, self).__init__(parent)
        # 定义图片列表标签
        self.label_image_list_box = tk.Label(self.image_option, text="已选择图片列表：")
        self.label_image_list_box.grid(row=0, column=0, columnspan=3, sticky="NW")
        # 定义图片列表，Listbox中添加export_selection关键字目的是解决两个listbox相互影响的问题
        self.image_list_box = tk.Listbox(self.image_option, height=20, width=50, exportselection=False)
        self.image_list_box.grid(row=1, column=0, columnspan=3)
        # 为图片列表绑定滚动条
        self.image_list_box_vertical_bar = tk.Scrollbar(self.image_option, orient='vertical',
                                                        command=self.image_list_box.yview)
        self.image_list_box_vertical_bar.grid(row=1, column=3, sticky='ns')
        self.image_list_box.configure(yscrollcommand=self.image_list_box_vertical_bar.set)

        self.image_list_box_horizontal_bar = tk.Scrollbar(self.image_option, orient='horizontal',
                                                          command=self.image_list_box.xview)
        self.image_list_box_horizontal_bar.grid(row=4, column=0, columnspan=3, sticky='we')
        self.image_list_box.configure(xscrollcommand=self.image_list_box_horizontal_bar.set)
        # 绑定加载列表项功能
        self.image_list_box.bind("<<ListboxSelect>>", self.display_image)
        # 选择图片按钮
        self.Choose_image = Button(self.image_option, command=self.choose_pic, text="添加图片", width=8, height=1)
        self.Choose_image.grid(row=5, column=0, sticky=tk.N)
        # 删除图片按钮
        self.Delete_image_button = Button(self.image_option, command=self.delete_image, text="删除图片", width=8, height=1)
        self.Delete_image_button.grid(row=5, column=1, sticky=tk.N)
        # 清空列表按钮
        self.Clear_image_button = Button(self.image_option, command=self.clear_images, text="清空列表", width=8, height=1)
        self.Clear_image_button.grid(row=5, column=2, sticky=tk.N)

    # 选择图片事件
    def choose_pic(self):
        self.filenames.clear()
        self.filenames += filedialog.askopenfilenames(title='Please choose a picture', initialdir='/',
                                                      filetypes=[('图片文件', '*.png'), ('图片文件', '*.jpg')])
        for filename in self.filenames:
            if filename in self.filenames_list:
                self.filenames.pop(self.filenames.index(filename))
        self.filenames_list += self.filenames
        for item in self.filenames:
            self.image_label_list.append([])
            self.image_list_box.insert(tk.END, item)

    # 删除图片事件
    def delete_image(self):
        if self.index is not None:
            # 删除canvas中所有组件
            self.canvas.delete(tk.ALL)
            # 清空图片list_box
            self.image_list_box.delete(0, END)
            self.filenames_list.pop(self.index[0])
            self.image_label_list.pop(self.index[0])
            for item in self.filenames_list:
                self.image_list_box.insert(tk.END, item)

    # 清空图片列表事件
    def clear_images(self):
        if len(self.filenames_list) != 0:
            # 删除canvas中所有组件
            self.canvas.delete(tk.ALL)
            # 清空图片list_box
            self.image_list_box.delete(0, END)
            # 清空图片列表
            self.filenames.clear()
            self.filenames_list.clear()
            # 关键点列表清空
            self.image_label_list.clear()
            # 关键点canvas中坐标列表清空
            self.points_list.clear()
            # 关键点列表下标归零
            self.label_index = 0
            self.index = None
            self.delete_point_index = None
            # 清空关键点list_box
            self.label_list_box.delete(0, END)

    # 显示图片事件
    def display_image(self, event):
        self.path = event.widget
        # 放置重新载入正在显示的图像
        if self.index != self.path.curselection():
            self.index = self.path.curselection()
            # 放置点击空白list_box报错
            if len(self.index) == 0:
                return
            # 清空框架中的内容
            self.canvas.delete(tk.ALL)
            self.label_list_box.delete(0, tk.END)
            self.points_list.clear()
            # 重新定义canvas，使canvas回到初始位置
            self.canvas = tk.Canvas(self.inner, height=self.root_windows_height - 100,
                                    width=self.root_windows_width - 400,
                                    background="white")
            self.canvas.grid(row=0, column=0, rowspan=10)
            self.canvas.bind("<MouseWheel>", self.zoom_windows)
            self.canvas.bind("<ButtonPress-1>", self.move_start)
            self.canvas.bind("<B1-Motion>", self.move_move)
            self.canvas.bind("<Button-3>", self.draw_point)
            self.scale = 1
            # 布局所选图片
            self.image1 = Image.open(self.path.get(self.index))
            # 获取图片分辨率
            self.image_true_width = self.image1.width
            self.image_true_height = self.image1.height
            # 若图片过大，则先缩小至1/4
            if self.image_true_width >= 1000 or self.image_true_height >= 1500:
                self.image1 = self.image1.resize((int(self.image_true_width/2), int(self.image_true_height/2)))
                self.image_width = int(self.image_true_width / 2)
                self.image_height = int(self.image_true_height / 2)
            else:
                self.image_width = self.image_true_width
                self.image_height = self.image_true_height
            # 将图片放置到画布上
            self.image = ImageTk.PhotoImage(self.image1)
            self.canvas.create_image((self.root_windows_width - 400) / 2, (self.root_windows_height - 100) / 2,
                                     image=self.image)
            # 图片中心在画布上的坐标
            self.image_x = (self.root_windows_width - 400) / 2
            self.image_y = (self.root_windows_height - 100) / 2
            # 显示已画点
            if len(self.image_label_list[self.index[0]]) != 0:
                for item in self.image_label_list[self.index[0]]:
                    self.label_list_box.insert(tk.END, item)
                    self.label_index = item[0] + 1
                    point_x = item[1] / 2 + self.image_x - self.image_width / 2
                    point_y = item[2] / 2 + self.image_y - self.image_height / 2
                    self.canvas.create_oval(point_x - self.points_radius, point_y - self.points_radius,
                                            point_x + self.points_radius, point_y + self.points_radius, fill="red",
                                            activefill="blue")
                    # 将以画点的canvas坐标存入列表
                    self.points_list.append([point_x, point_y])
            else:
                self.label_index = 0














