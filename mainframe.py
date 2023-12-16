import tkinter as tk
from tkinter import ttk


class ScrolledFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.filenames = []     # 最近一次添加图片的列表
        self.filenames_list = []    # 图片列表
        self.image_label_list = []  # 所有图片关键点列表
        self.points_list = []   # canvas的点坐标
        self.image = None   # 放入canvas中的图片
        self.image1 = None  # 读取的图片
        self.path = None    # 图片路径
        self.index = None  # 图片下标
        self.insert_point_flag = 0  # 插入关键点标识
        self.delete_point_index = None  # 选中待删除关键点下标
        self.points_radius = 2  # 关键点半径
        self.label_index = 0    # 每张图片关键点下标
        self.image_x = 0        # 图片中心坐标x
        self.image_y = 0        # 图片中心坐标y
        self.image_width = 0    # 图片宽度
        self.image_height = 0   # 图片高度
        self.image_true_width = 0   # 真实图片宽度
        self.image_true_height = 0  # 真实图片高度
        self.scale = 1  # 缩放背书
        self.model = 0  # 选择标注关键点的数量
        # 获取屏幕的宽高
        self.root_windows_width = parent.winfo_screenwidth()
        self.root_windows_height = parent.winfo_screenheight()

        # 最外层定义，用于窗口滚动条
        self._canvas = tk.Canvas(self)
        self._canvas.grid(row=0, column=0, sticky='news')
        # 创建右滚动条并连接到画布右侧
        self._vertical_bar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)
        self._vertical_bar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)
        # 创建底部滚动条并连接到画布下侧
        self._horizontal_bar = tk.Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        self._horizontal_bar.grid(row=1, column=0, sticky='we')
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

        # 定义内部框架
        self.inner = tk.Frame(self._canvas)
        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')
        # 自动调整内部框架大小
        self.columnconfigure(0, weight=1)  # changed
        self.rowconfigure(0, weight=1)  # changed
        self.inner.bind('<Configure>', self.resize)

        # 画布模块
        self.canvas = tk.Canvas(self.inner, height=self.root_windows_height - 100, width=self.root_windows_width - 400,
                                background="white")
        self.canvas.grid(row=0, column=0, rowspan=10)
        # 图片选择模块
        self.image_option = tk.Frame(self.inner)
        self.image_option.grid(row=1, column=1, columnspan=3)

        # 选择标注模式文本
        self.label3 = tk.Label(self.inner, text="请选择标注模式：")
        self.label3.grid(row=3, column=1)
        # 选择标注模式下拉列表
        self.modelList = ttk.Combobox(self.inner)  # 初始化
        self.modelList["values"] = ("--请选择标注模式--", "5点", "68点", "98点", "自定义")
        self.modelList.current(0)  # 选择第一个
        self.modelList.bind("<<ComboboxSelected>>", self.model_select)
        self.modelList.grid(row=3, column=2)
        # 预标注按钮
        self.annotation_button = tk.Button(self.inner, text="预标注", command=self.annotation, width=8, height=1)
        self.annotation_button.grid(row=3, column=3, sticky=tk.NW)
        self.annotation_button.config(state=tk.DISABLED)

        # 关键点标注信息模块
        self.label_option = tk.Frame(self.inner)
        self.label_option.grid(row=5, column=1, columnspan=3)
        # 定义关键点列表
        self.label_list_box = tk.Listbox(self.label_option, height=20, width=50, exportselection=False)
        self.label_list_box.grid(row=1, column=0, columnspan=3)

    # 窗口大小事件
    def resize(self, event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

    def model_select(self, event):
        model_name = self.modelList.get()
        if model_name == "5点":
            self.model = 1
            self.annotation_button.config(state=tk.ACTIVE)
        elif model_name == "68点":
            self.model = 2
            self.annotation_button.config(state=tk.ACTIVE)
        elif model_name == "98点":
            self.model = 3
            self.annotation_button.config(state=tk.ACTIVE)
        elif model_name == "自定义":
            self.model = 4
            self.annotation_button.config(state=tk.DISABLED)

    def annotation(self):
        if self.image  is not None and self.model is not 4:
            if self.model == 1:
                pass
            elif self.model == 2:
                pass
            elif self.model == 3:
                pass
            elif self.model == 4:
                pass







