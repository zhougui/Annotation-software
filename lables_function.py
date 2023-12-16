import math

from ui.pictures_function import PicturesFunction
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import time
import xlsxwriter

class LabelsFunction(PicturesFunction):
    def __init__(self, parent):
        super(LabelsFunction, self).__init__(parent)
        # 定义选中的关键点
        self.selected_points = []
        # 定义关键点列表标签
        self.label_label_list_box = tk.Label(self.label_option, text="关键点坐标列表：")
        self.label_label_list_box.grid(row=0, column=0, columnspan=3, sticky="NW")
        # 为关键点列表添加滚动条
        self.label_list_box_vertical_bar = tk.Scrollbar(self.label_option, orient='vertical',
                                                        command=self.label_list_box.yview)
        self.label_list_box_vertical_bar.grid(row=1, column=3, sticky='ns')
        self.label_list_box.configure(yscrollcommand=self.label_list_box_vertical_bar.set)
        # 绑定点击关键点事件
        self.label_list_box.bind("<<ListboxSelect>>", self.display_point)
        # 删除关键信息按钮
        self.delete_point_button = Button(self.label_option, command=self.delete_point, text="删除关键点", width=10,
                                          height=1)
        self.delete_point_button.grid(row=5, column=0, sticky=tk.N)
        # 插入关键信息按钮
        self.insert_point_button = Button(self.label_option, command=self.insert_point, text="插入关键点", width=10,
                                          height=1)
        self.insert_point_button.grid(row=5, column=1, sticky=tk.N)
        # 清空关键点列表按钮
        self.clear_points_list_box = Button(self.label_option, command=self.clear_points, text="清空列表", width=8,
                                            height=1)
        self.clear_points_list_box.grid(row=5, column=2, sticky=tk.N)

        # 空标签，用于填充
        self.label1 = tk.Label(self.label_option, text=" ")
        self.label1.grid(row=6, column=0, sticky="NW")
        # 加载标注文件按钮
        self.load_label = Button(self.label_option, command=self.load_file, text="加载文件", width=8, height=1)
        self.load_label.grid(row=7, column=0, sticky=tk.NE)
        # 保存关键点信息按钮
        self.save_points_button = Button(self.label_option, command=self.save_points, text="保存", width=8, height=1)
        self.save_points_button.grid(row=7, column=2, sticky=tk.NW)
        # 计算距离角度按钮
        self.calculate_button = Button(self.label_option, command=self.select_calculation, text="计算", width=8, height=1)
        self.calculate_button.grid(row=7, column=1, sticky=tk.NS)

# 高亮选中关键点事件
    def display_point(self, event):
        # 获取列表中选中信息
        points_list = event.widget
        index = points_list.curselection()
        # 放置点击空白list_box报错
        if len(index) != 0:
            # 删除canvas中所有组件
            self.canvas.delete(tk.ALL)
            # 重新载入图像
            self.canvas.create_image(self.image_x, self.image_y, image=self.image)
            self.delete_point_index = index[0]
            # 重新载入以画关键点
            for points_index in range(len(self.points_list)):
                # 获取canvas上关键点坐标
                point_x = self.points_list[points_index][0]
                point_y = self.points_list[points_index][1]
                self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                        point_y - self.points_radius * self.scale,
                                        point_x + self.points_radius * self.scale,
                                        point_y + self.points_radius * self.scale, fill="red",
                                        activefill="blue")
            # 将选中的点设为蓝色
            point_x = self.points_list[index[0]][0]
            point_y = self.points_list[index[0]][1]
            self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                    point_y - self.points_radius * self.scale,
                                    point_x + self.points_radius * self.scale,
                                    point_y + self.points_radius * self.scale, fill="blue")

    # 保存关键点信息
    def save_points(self):
        # point_name = ["0","1","右耳屏前点", "右下颌角点", "颏下点", "左下颌角点", "左耳屏前点", "鼻根点", "鼻尖点", "右鼻翼点", "鼻下点", "左鼻翼点", "右外眦点", "右上睑缘中点",
        #               "右內眦点", "右下睑缘中点", "左內眦点", "左上睑缘中点", '左外眦点', "左下睑缘中点", "右口角点", "上唇缘中点", "左口角点", "下唇缘中点", "上唇下缘中点",
        #               "下唇上缘中点", "右瞳孔点", "左瞳孔点", "上中切牙点", "下中切牙点", "上唇凹点", "下唇凹点", "颏前点", "颏点"]
        point_name = ["右侧口角点", "右唇峰点", "唇珠", "左唇峰点", "左侧口角点", "下唇中点", "上唇下缘中点", "下唇上缘中点","13中点",
                        "12中点", "11中点", "21中点", "22中点", "23中点", "13下唇点", "12下唇点", "11下唇点", "21下唇点",
                        "22下唇点", "23下唇点"]
        for item in self.image_label_list:
            if len(item) > 0:
                save_path = filedialog.asksaveasfilename(filetypes=[('txt文件', '*.txt')])
                real_time = time.time()
                real_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(real_time))
                fp = open(save_path + "-" + real_time + ".txt", "w+", encoding="utf-8")
                xls = xlsxwriter.Workbook(save_path + "-" + real_time + ".xls")
                for info in range(len(self.image_label_list)):
                    if len(self.image_label_list[info]) > 0:
                        photo_name = self.filenames_list[info].split('/')
                        sht = xls.add_worksheet(photo_name[-1])
                        sht.write(0, 0, '序号')
                        sht.write(0, 1, '名称')
                        sht.write(0, 2, 'X')
                        sht.write(0, 3, 'Y')
                        for [i, x, y] in self.image_label_list[info]:
                            fp.write(str(x) + " " + str(y) + " ")
                            sht.write(i+1, 0, i+1)
                            sht.write(i+1, 1, point_name[i])
                            sht.write(i+1, 2, str(x))
                            sht.write(i+1, 3, str(y))
                        fp.write(photo_name[-1] + "\n")
                for i in range(len(point_name)):
                    if i != 22 and i != 23:
                        sht = xls.add_worksheet(point_name[i])
                        sht.write(0, 0, '序号')
                        sht.write(0, 1, '名称')
                        sht.write(0, 2, 'X')
                        sht.write(0, 3, 'Y')
                        for info in range(len(self.image_label_list)):
                            messsage = self.image_label_list[info]
                            photo_name = self.filenames_list[info].split('/')[-1]
                            sht.write(info + 1, 0, info + 1)
                            sht.write(info + 1, 1, photo_name)
                            if i < len(messsage):
                                sht.write(info + 1, 2, str(messsage[i][1]))
                                sht.write(info + 1, 3, str(messsage[i][2]))
                fp.close()
                xls.close()
                return

    # 在新窗口中选择计算距离或计算角度
    def select_calculation(self):
        # 清除canvas上所有的线段
        self.canvas.delete("line")
        self.calculation_window = Toplevel(self.label_option)
        self.calculation_window.title("计算类型选择")
        self.calculation_window.geometry("300x200")  # 设置窗口大小

        calculations = ["距离", "角度"]
        selected_calculation = StringVar()

        # 创建单选按钮来选择计算类型
        for calc in calculations:
            Radiobutton(self.calculation_window, text=calc, variable=selected_calculation, value=calc).pack()

        # 创建确认按钮以执行计算
        confirm_button = tk.Button(self.calculation_window, text="执行计算",
                                       command=lambda: self.calculate(selected_calculation.get()))
        confirm_button.pack()

    # 根据选择的计算类型执行计算
    def calculate(self, calculation_type):
        if calculation_type == "距离":
            # 销毁原来的窗口
            self.calculation_window.destroy()
            # 创建新的窗口用于选择要计算的两个点
            self.point_selection_window = Toplevel(self.master)
            self.point_selection_window.title("选择要计算的点")
            self.point_selection_window.geometry("300x200")  # 设置窗口大小

            def on_select(event):
                # 更新选定的点
                selected_index = points_listbox.curselection()
                self.selected_points = [int(points_listbox.get(i)) for i in selected_index]

            scroll_y = Scrollbar(self.point_selection_window, orient="vertical")
            points_listbox = Listbox(self.point_selection_window, selectmode="multiple", yscrollcommand=scroll_y.set)

            for i in range(34):
                points_listbox.insert(tk.END, str(i))

            scroll_y.config(command=points_listbox.yview)
            points_listbox.bind("<<ListboxSelect>>", on_select)

            scroll_y.pack(side="right", fill="y")
            points_listbox.pack(side="left", fill="both", expand=True)

            # 创建确认按钮以执行计算，并读取选择的两个点
            confirm_button = tk.Button(self.point_selection_window, text="执行计算",
                                       command=lambda: self.calculate_distance(self.selected_points))
            confirm_button.pack(pady=10)

        elif calculation_type == "角度":
            # 销毁原始窗口
            self.calculation_window.destroy()
            # 创建新窗口以选择点
            self.point_selection_window = Toplevel(self.master)
            self.point_selection_window.title("选择要计算的点")
            self.point_selection_window.geometry("500x400")

            def on_select(event):
                selected_index = points_listbox.curselection()
                self.selected_points = [int(points_listbox.get(i)) for i in selected_index]

            scroll_y = Scrollbar(self.point_selection_window, orient="vertical")
            points_listbox = Listbox(self.point_selection_window, selectmode="multiple", yscrollcommand=scroll_y.set)

            for i in range(34):
                points_listbox.insert(tk.END, str(i))

            scroll_y.config(command=points_listbox.yview)
            points_listbox.bind("<<ListboxSelect>>", on_select)

            scroll_y.pack(side="right", fill="y")
            points_listbox.pack(side="left", fill="both", expand=True)

            # 创建按钮以进入下一步
            confirm_button = tk.Button(self.point_selection_window, text="下一步",
                                       command=lambda: self.select_vertex_for_angle(self.selected_points))
            confirm_button.pack(pady=20)

        else:
            result = "请选择计算类型"
            # 在这里可以显示计算结果，例如一个标签或者对话框
            result_label = tk.Label(self.master, text=result)
            result_label.pack()

    # 距离计算，使用选定的两个点的索引
    def calculate_distance(self, selected_points):
        # 在绘制线段时，清除之前的绘制
        self.clear_drawn_lines()
        if len(selected_points) == 2:
            point1_index, point2_index = selected_points[0], selected_points[1]
            #print(self.image_label_list[self.index[0]][point1_index],self.image_label_list[self.index[0]][point2_index])
            #print(self.image_label_list[self.index[0]][32],self.image_label_list[self.index[0]][33])
            x1 = self.image_label_list[self.index[0]][point1_index][1]
            x2 = self.image_label_list[self.index[0]][point2_index][1]
            y1 = self.image_label_list[self.index[0]][point1_index][2]
            y2 = self.image_label_list[self.index[0]][point2_index][2]
            x__0 = self.image_label_list[self.index[0]][0][1]
            x__1 = self.image_label_list[self.index[0]][1][1]
            y__0 = self.image_label_list[self.index[0]][0][2]
            y__1 = self.image_label_list[self.index[0]][1][2]
            distance = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
            distance_scale = math.sqrt(pow(x__1 - x__0, 2) + pow(y__1 - y__0, 2))
            distance_real = distance / distance_scale
            # 画出线段
            self.draw_line(x1, y1, x2, y2)
            # 显示计算结果
            result = f"计算出的距离为: {distance_real}"
            result_label = tk.Label(self.point_selection_window, text=result)
            result_label.pack()
        else:
            result = "请选择两个点进行距离计算"
            # 在这里可以显示计算结果，例如一个标签或者对话框
            result_label = tk.Label(self.point_selection_window, text=result)
            result_label.pack(pady=10)

    def select_vertex_for_angle(self,selected_points):
        self.point_selection_window.destroy()
        # 检查是否选择了恰好三个点
        if len(selected_points) != 3:
            result = "请选择三个点"
        else:
            # 创建一个新窗口以选择顶点
            self.vertex_selection_window = Toplevel(self.master)
            self.vertex_selection_window.title("选择顶点")
            self.vertex_selection_window.geometry("300x300")

            self.selected_vertex = None

            def on_select(event):
                selected_index = vertex_listbox.curselection()
                self.selected_vertex = int(vertex_listbox.get(selected_index))

            vertex_listbox = Listbox(self.vertex_selection_window)
            for i in self.selected_points:
                vertex_listbox.insert(tk.END, str(i))

            vertex_listbox.bind("<<ListboxSelect>>", on_select)
            vertex_listbox.pack()

            # 创建按钮以计算角度
            confirm_button = tk.Button(self.vertex_selection_window, text="计算角度",
                                       command=lambda: self.calculate_angle())
            confirm_button.pack(pady=10)

    def calculate_angle(self):
        #print(self.selected_points)
        #print(self.selected_vertex)
        # 点位于二维空间中，使用三角函数计算角度
        point1_index, point2_index,point3_index = self.selected_points[0], self.selected_points[1],self.selected_points[2]
        vertex_point_index = self.selected_vertex
        x1, y1 = self.image_label_list[self.index[0]][point1_index][1], self.image_label_list[self.index[0]][point1_index][2]
        x2, y2 = self.image_label_list[self.index[0]][point2_index][1], self.image_label_list[self.index[0]][point2_index][2]
        x3, y3 = self.image_label_list[self.index[0]][point3_index][1], self.image_label_list[self.index[0]][point3_index][2]
        #print(x1,y1,x2,y2,x3,y3)
        if vertex_point_index==point1_index:
            vertex_x, vertex_y = x1, y1
            angle = self.calculate_angle_logic(x2, y2,vertex_x, vertex_y, x3, y3)
        elif vertex_point_index==point2_index:
            vertex_x, vertex_y = x2, y2
            angle = self.calculate_angle_logic(x1, y1, vertex_x, vertex_y, x3, y3)
        else:
            vertex_x, vertex_y = x3, y3
            angle = self.calculate_angle_logic(x1, y1, vertex_x, vertex_y, x2, y2)
        #print(angle)
        result = f"计算出的角度为: {angle}"
        # 在标签中显示结果
        result_label = tk.Label(self.vertex_selection_window, text=result)
        result_label.pack(pady=10)

    def calculate_angle_logic(self,x1, y1, x2, y2, x3, y3):
        # 在绘制线段时，清除之前的绘制
        self.clear_drawn_lines()
        # 计算向量 BA 和向量 BC 的内积
        dot_product = (x1 - x2) * (x3 - x2) + (y1 - y2) * (y3 - y2)

        # 计算向量 BA 的模和向量 BC 的模
        magnitude_ab = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        magnitude_bc = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)

        # 计算夹角的余弦值
        cos_theta = max(min(dot_product / (magnitude_ab * magnitude_bc), 1.0), -1.0)

        # 使用反余弦函数计算夹角（弧度）
        theta_radians = math.acos(cos_theta)

        # 将弧度转换为角度
        theta_degrees = math.degrees(theta_radians)
        self.draw_angle(x1, y1, x2, y2, x3, y3)
        return theta_degrees

    def clear_drawn_lines(self):
        for line in self.drawn_lines:
            self.canvas.delete(line)
        self.drawn_lines = []

    # 插入关键点
    def insert_point(self):
        # 插入关键点表标识置1
        self.insert_point_flag = 1

    # 删除选中关键点列表按钮事件
    def delete_point(self):
        if self.delete_point_index is not None:
            # 删除canvas中所有组件
            self.canvas.delete(tk.ALL)
            # 重新载入图像
            self.canvas.create_image(self.image_x, self.image_y, image=self.image)
            # 关键点列表删除选中关键点
            self.image_label_list[self.index[0]].pop(self.delete_point_index)
            for i in range(self.delete_point_index, len(self.image_label_list[self.index[0]])):
                self.image_label_list[self.index[0]][i][0] -= 1
            # 关键点canvas中坐标列表删除选中关键点
            self.points_list.pop(self.delete_point_index)
            # 关键点列表下标-1
            self.label_index -= 1
            # 清空关键点list_box
            self.label_list_box.delete(0, END)
            # 重新插入list_box
            for item in self.image_label_list[self.index[0]]:
                self.label_list_box.insert(tk.END, item)
            # 重新载入以画关键点
            for points_index in range(len(self.points_list)):
                # 获取canvas上关键点坐标
                point_x = self.points_list[points_index][0]
                point_y = self.points_list[points_index][1]
                self.canvas.create_oval(point_x - self.points_radius * self.scale,
                                        point_y - self.points_radius * self.scale,
                                        point_x + self.points_radius * self.scale,
                                        point_y + self.points_radius * self.scale, fill="red",
                                        activefill="blue")
            # 为了插入点时重新对delete_point_index进行判断
            self.delete_point_index = None

    # 清空关键点列表按钮事件
    def clear_points(self):
        # 删除canvas中所有组件
        self.canvas.delete(tk.ALL)
        # 重新载入图像
        self.canvas.create_image(self.image_x, self.image_y, image=self.image)
        # 关键点列表清空
        self.image_label_list[self.index[0]].clear()
        # 关键点canvas中坐标列表清空
        self.points_list.clear()
        # 关键点列表下标归零
        self.label_index = 0
        # 清空关键点list_box
        self.label_list_box.delete(0, END)

    # 加载文件事件
    def load_file(self):
        label_file = filedialog.askopenfilename(title='选择一个txt格式数据集文件', initialdir='/',
                                                filetypes=[('txt', '*.txt')])
        fp = open(label_file, "r", encoding="utf-8")
        self.clear_images()
        for label in fp:
            label_info = label.split(' ')
            label_files = label_file.split('/')
            label_files[-1] = label_info[-1]
            filename = "/".join(label_files).replace('\n', '').replace('\r', '')
            self.filenames.append(filename)
            labels = []
            for i in range(int(len(label_info) / 2)):
                if i < 34:
                    labels.append([i, float(label_info[i * 2]), float(label_info[i * 2 + 1])])
            self.image_label_list.append(labels)
        self.filenames_list += self.filenames
        for item in self.filenames:
            self.image_list_box.insert(tk.END, item)
        # for item in self.image_label_list:
        #     print(item)

















