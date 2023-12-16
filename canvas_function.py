from ui.mainframe import ScrolledFrame
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class CanvasFunction(ScrolledFrame):
    def __init__(self, parent):
        super(CanvasFunction, self).__init__(parent)

        # 绑定缩放
        self.canvas.bind("<MouseWheel>", self.zoom_windows)
        # 绑定左键移动
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        # 绑定右键画点
        self.canvas.bind("<Button-3>", self.draw_point)
        self.drawn_lines = []
        # 画点时的比例
        self.scaled_points = 1
        # 鼠标相对坐标
        self.mouse_x = 0
        self.mouse_y = 0
        #坐标变换系数
        self.a = 1
        self.bx = 0
        self.by = 0

    # 移动canvas事件
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # 窗口缩放事件
    def zoom_windows(self, event):
        # 获取相对坐标
        # true_x = self.canvas.canvasx(event.x)
        # true_y = self.canvas.canvasy(event.y)
        true_x = 732.0
        true_y = 542.0
        # 当canvas中有图片,且鼠标在图像内时，才可以缩放（缩放的原理是重新放置改变大小后的图片）
        if self.image1 is not None and self.image_x - self.image_width / 2 <= true_x <= self.image_x + self.image_width / 2 and self.image_y - self.image_height / 2 <= true_y <= self.image_y + self.image_height / 2:
            # 鼠标滚轮向上，放大
            if event.delta > 0 and self.scale <= 3:
                # 删除canvas中所有组件
                self.canvas.delete(tk.ALL)
                self.image1 = Image.open(self.path.get(self.index))
                # 图像高宽放大1.1倍
                self.image_width = int(self.image_width * 1.1)
                self.image_height = int(self.image_height * 1.1)
                # 图像的中心坐标
                self.image_x = (self.image_x - true_x) * 1.1 + true_x
                self.image_y = (self.image_y - true_y) * 1.1 + true_y
                self.image1 = self.image1.resize((self.image_width, self.image_height))
                self.image = ImageTk.PhotoImage(self.image1)
                self.canvas.create_image(self.image_x, self.image_y, image=self.image)
                if len(self.points_list) != 0:
                    # canvas的点坐标下标
                    for points_index in range(len(self.points_list)):
                        # 获取canvas上关键点坐标
                        point_x = self.points_list[points_index][0]
                        point_y = self.points_list[points_index][1]
                        point_x = (point_x - true_x) * 1.1 + true_x
                        point_y = (point_y - true_y) * 1.1 + true_y
                        self.points_list[points_index][0] = point_x
                        self.points_list[points_index][1] = point_y
                        self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                                point_y - self.points_radius * self.scale,
                                                point_x + self.points_radius * self.scale,
                                                point_y + self.points_radius * self.scale, fill="red",
                                                activefill="blue")
                # 缩放倍数扩大1.1倍
                self.scale *= 1.1
            elif event.delta < 0 and self.scale > 0.6:
                # 删除canvas中所有组件
                self.canvas.delete(tk.ALL)
                self.image1 = Image.open(self.path.get(self.index))
                self.image_width = int(self.image_width / 1.1)
                self.image_height = int(self.image_height / 1.1)
                self.image_x = (self.image_x - true_x) / 1.1 + true_x
                self.image_y = (self.image_y - true_y) / 1.1 + true_y
                self.image1 = self.image1.resize((self.image_width, self.image_height))
                self.image = ImageTk.PhotoImage(self.image1)
                self.canvas.create_image(self.image_x, self.image_y, image=self.image)
                if len(self.points_list) != 0:
                    # canvas的点坐标下标
                    for points_index in range(len(self.points_list)):
                        # 获取canvas上关键点坐标
                        point_x = self.points_list[points_index][0]
                        point_y = self.points_list[points_index][1]
                        point_x = (point_x - true_x) / 1.1 + true_x
                        point_y = (point_y - true_y) / 1.1 + true_y
                        self.points_list[points_index][0] = point_x
                        self.points_list[points_index][1] = point_y
                        self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                                point_y - self.points_radius * self.scale,
                                                point_x + self.points_radius * self.scale,
                                                point_y + self.points_radius * self.scale, fill="red",
                                                activefill="blue")
                self.scale /= 1.1
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.mouse_x = true_x
        self.mouse_y = true_y
        # print("mouse:",self.mouse_x,self.mouse_y)

    # 画点事件
    def draw_point(self, event):
        self.mouse_x = 0
        self.mouse_y = 0
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        #print("true_x,true_y:",true_x,true_y)
        if self.label_index < 34 and self.image1 is not None:
            # 得到点在真实图片坐标系下的坐标
            point_x = (true_x - self.image_x + self.image_width / 2) / self.image_width * self.image_true_width
            point_y = (true_y - self.image_y + self.image_height / 2) / self.image_height * self.image_true_height
            self.a = self.image_true_width/self.image_width
            self.bx = (self.image_width / 2 - self.image_x) / self.image_width * self.image_true_width
            self.by = (self.image_height / 2 - self.image_y) / self.image_height * self.image_true_height
            #print("point_x, point_y:",point_x, point_y)
            # 保留两位有效数字
            point_x = round(point_x, 2)
            point_y = round(point_y, 2)
            if 0 <= point_x <= self.image_true_width and 0 <= point_y <= self.image_true_height:
                self.canvas.create_oval(true_x - self.points_radius * self.scale,
                                        true_y - self.points_radius * self.scale,
                                        true_x + self.points_radius * self.scale,
                                        true_y + self.points_radius * self.scale, fill="red", activefill="blue")
                # 插入点时的画点操作
                if self.delete_point_index is not None and self.insert_point_flag == 1:
                    self.insert_point_flag = 0
                    self.image_label_list[self.index[0]].insert(self.delete_point_index,
                                                                [self.delete_point_index, point_x, point_y])
                    self.points_list.insert(self.delete_point_index, [true_x, true_y])
                    # 删除canvas中所有组件
                    self.canvas.delete(tk.ALL)
                    # 重新载入图像
                    self.canvas.create_image(self.image_x, self.image_y, image=self.image)
                    for points_index in range(len(self.points_list)):
                        # 获取canvas上关键点坐标
                        point_x = self.points_list[points_index][0]
                        point_y = self.points_list[points_index][1]
                        self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                                point_y - self.points_radius * self.scale,
                                                point_x + self.points_radius * self.scale,
                                                point_y + self.points_radius * self.scale, fill="red",
                                                activefill="blue")
                    # 更改关键点列表中的index值
                    for i in range(self.delete_point_index + 1, len(self.image_label_list[self.index[0]])):
                        self.image_label_list[self.index[0]][i][0] += 1
                    # 清空关键点list_box
                    self.label_list_box.delete(0, END)
                    # 重新插入list_box
                    for item in self.image_label_list[self.index[0]]:
                        self.label_list_box.insert(tk.END, item)
                    self.delete_point_index = None
                # 追加画点的操作
                else:
                    self.image_label_list[self.index[0]].append([self.label_index, point_x, point_y])
                    self.points_list.append([true_x, true_y])
                    self.label_list_box.insert(tk.END, self.image_label_list[self.index[0]][self.label_index])
                self.label_index += 1
        self.point_image_x = self.image_x
        self.point_image_y = self.image_y
        self.scaled_points = self.scale

    def canvas_to_image_coordinates(self, x, y):
        # 将画布坐标转换为图片坐标
        true_x = (x - self.bx) / self.a
        true_y = (y - self.by) / self.a
        if self.mouse_x != 0:
            true_x = (true_x - self.mouse_x) * self.scale / self.scaled_points + self.mouse_x
            true_y = (true_y - self.mouse_y) * self.scale / self.scaled_points + self.mouse_y
        return true_x, true_y

    def draw_line(self, x1, y1, x2, y2):
        true_x1, true_y1 = self.canvas_to_image_coordinates(x1, y1)
        true_x2, true_y2 = self.canvas_to_image_coordinates(x2, y2)
        # 绘制起点和终点
        line = self.canvas.create_line(true_x1, true_y1, true_x2, true_y2, fill="blue",width=2)
        self.drawn_lines.append(line)

    def draw_angle(self, x1, y1, x2, y2, x3, y3):
        # 画出角度
        true_x1, true_y1 = self.canvas_to_image_coordinates(x1, y1)
        true_x2, true_y2 = self.canvas_to_image_coordinates(x2, y2)
        true_x3, true_y3 = self.canvas_to_image_coordinates(x3, y3)
        # 计算角度的顶点
        vertex_x, vertex_y = true_x2, true_y2
        # 计算角度的另外两个点
        p1_x, p1_y = true_x1, true_y1
        p2_x, p2_y = true_x3, true_y3
        # 画出角度
        line1 = self.canvas.create_line(p1_x, p1_y, vertex_x, vertex_y, fill="green", width=2)
        line2 = self.canvas.create_line(p2_x, p2_y, vertex_x, vertex_y, fill="green", width=2)
        self.drawn_lines.append(line1)
        self.drawn_lines.append(line2)

    def clear_lines(self):
        # 清除canvas上所有的线段
        self.canvas.delete("line")
















