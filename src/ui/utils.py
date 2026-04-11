import tkinter as tk
from tkinter import ttk

def configure_treeview_center(tree):
    """配置Treeview表格数据居中显示"""
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Item", anchor=tk.CENTER)
    style.configure("Treeview.Heading", anchor=tk.CENTER)
    
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)

def configure_treeview_grid(tree):
    """配置Treeview表格显示网格线"""
    style = ttk.Style()
    style.configure("Treeview", 
                    rowheight=25,
                    borderwidth=1,
                    relief=tk.GROOVE)
    style.configure("Treeview.Item",
                    borderwidth=1,
                    relief=tk.GROOVE)