import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.utils import configure_treeview_center

class TextImportDialog:
    def __init__(self, parent, people):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("粘贴文本导入业绩")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.people = people
        
        ttk.Label(self.dialog, text="说明：识别'姓名'列和业绩列（列名可自定义）").pack(padx=5, pady=5)
        
        label_frame = ttk.Frame(self.dialog)
        label_frame.pack(padx=5, pady=5)
        ttk.Label(label_frame, text="业绩列名：").pack(side=tk.LEFT)
        self.performance_label_entry = ttk.Entry(label_frame, width=15)
        self.performance_label_entry.insert(0, "累计业绩")
        self.performance_label_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dialog, text="示例：姓名\t累计业绩").pack(padx=5)
        ttk.Label(self.dialog, text="      A\t40000").pack(padx=5)
        ttk.Label(self.dialog, text="      B\t20000").pack(padx=5)
        
        text_frame = ttk.Frame(self.dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = tk.Text(text_frame, height=20)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="识别解析", command=self.parse_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="确认结果", command=self.confirm).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dialog, text="识别结果：").pack(padx=5)
        
        result_frame = ttk.Frame(self.dialog)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_tree = ttk.Treeview(result_frame, columns=("姓名", "业绩", "状态"), show="headings", height=10)
        self.result_tree.heading("姓名", text="姓名")
        self.result_tree.heading("业绩", text="业绩")
        self.result_tree.heading("状态", text="状态")
        self.result_tree.column("姓名", width=150)
        self.result_tree.column("业绩", width=150)
        self.result_tree.column("状态", width=150)
        configure_treeview_center(self.result_tree)
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)
        
        ttk.Label(self.dialog, text="提示：状态为'已匹配'的人员已有身份配置").pack(padx=5)
        
        parent.wait_window(self.dialog)
    
    def parse_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("提示", "请先粘贴文本")
            return
        
        lines = text.split('\n')
        
        name_col_index = None
        performance_col_index = None
        
        for line in lines[:3]:
            cols = line.split('\t')
            for i, col in enumerate(cols):
                if col.strip() in ["姓名", "名字"]:
                    name_col_index = i
                elif col.strip() == self.performance_label_entry.get().strip():
                    performance_col_index = i
        
        if name_col_index is None:
            messagebox.showwarning("提示", "无法识别姓名列，请确保文本包含'姓名'列")
            return
        
        if performance_col_index is None:
            performance_label = self.performance_label_entry.get().strip()
            messagebox.showwarning("提示", f"无法识别业绩列，请确保文本包含'{performance_label}'列")
            return
        
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.parsed_data = {}
        
        for line in lines:
            cols = line.split('\t')
            if len(cols) > max(name_col_index, performance_col_index):
                name = cols[name_col_index].strip()
                performance_text = cols[performance_col_index].strip()
                
                if name and name not in ["姓名", "名字"]:
                    try:
                        performance = float(performance_text) if performance_text else 0.0
                        
                        person = next((p for p in self.people.values() if p.name == name), None)
                        status = "已匹配" if person else "未配置"
                        
                        self.parsed_data[name] = performance
                        self.result_tree.insert("", tk.END, values=(name, performance, status))
                    except ValueError:
                        pass
        
        if not self.parsed_data:
            messagebox.showwarning("提示", "未能识别任何有效数据")
        else:
            unmatched = sum(1 for item in self.result_tree.get_children() if self.result_tree.item(item)["values"][2] == "未配置")
            if unmatched > 0:
                messagebox.showinfo("识别完成", f"已识别{len(self.parsed_data)}条数据\n其中{unmatched}人未配置身份\n请确认后在人员管理中配置")
            else:
                messagebox.showinfo("识别完成", f"已识别{len(self.parsed_data)}条数据\n全部人员已匹配")
    
    def confirm(self):
        if not hasattr(self, 'parsed_data') or not self.parsed_data:
            messagebox.showwarning("提示", "请先点击'识别解析'按钮")
            return
        
        self.result = self.parsed_data
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()
