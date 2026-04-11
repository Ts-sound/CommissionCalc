import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("绩效提成计算系统")
        self.root.geometry("800x600")
        
        self._create_menu()
        self._create_main_frame()
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="导入业绩", command=self.import_performance)
        file_menu.add_command(label="导出结果", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        menubar.add_cascade(label="文件", menu=file_menu)
        
        self.root.config(menu=menubar)
    
    def _create_main_frame(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="绩效提成计算系统").grid(row=0, column=0)
        ttk.Label(main_frame, text="请导入Excel业绩文件开始计算").grid(row=1, column=0)
    
    def import_performance(self):
        pass
    
    def export_results(self):
        pass
    
    def run(self):
        self.root.mainloop()