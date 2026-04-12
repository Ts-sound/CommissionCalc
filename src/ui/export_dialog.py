import tkinter as tk
from tkinter import ttk, messagebox
from src.repositories.export_order_repo import ExportOrderRepository

class ExportDialog:
    def __init__(self, parent, people, config_dir):
        self.result = None
        self.order = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("导出结果")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.people = people
        self.export_order_repo = ExportOrderRepository(config_dir)
        
        ttk.Label(self.dialog, text="粘贴名单（每行一个姓名）").pack(padx=5, pady=5)
        
        text_frame = ttk.Frame(self.dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = tk.Text(text_frame, height=10)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="使用保存顺序", command=self.load_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存当前顺序", command=self.save_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="确认导出", command=self.confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dialog, text="提示：名单中不存在的人员数据补0").pack(padx=5)
        
        parent.wait_window(self.dialog)
    
    def load_order(self):
        names = self.export_order_repo.load()
        if names:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "\n".join(names))
            messagebox.showinfo("提示", f"已加载保存的顺序（{len(names)}人）")
        else:
            messagebox.showinfo("提示", "暂无保存的顺序")
    
    def save_order(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            names = [n.strip() for n in text.split('\n') if n.strip()]
            self.export_order_repo.save(names)
            messagebox.showinfo("提示", f"已保存顺序（{len(names)}人）")
        else:
            messagebox.showwarning("提示", "请先输入名单")
    
    def confirm(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            self.order = [n.strip() for n in text.split('\n') if n.strip()]
        self.result = True
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()