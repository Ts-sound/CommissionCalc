import tkinter as tk
from tkinter import ttk, messagebox
from src.models.person import Person
from src.models.role import Role
from src.models.group import Group
from src.models.commission import Tier, Bonus
import uuid

class PersonDialog:
    def __init__(self, parent, people, groups, person=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("添加/编辑人员")
        self.dialog.geometry("300x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.people = people
        self.groups = groups
        self.person = person
        
        ttk.Label(self.dialog, text="姓名：").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self.dialog)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="身份：").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.role_combo = ttk.Combobox(self.dialog, values=["总主管", "组长", "成员"], state="readonly")
        self.role_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="组别：").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        group_names = [g.name for g in groups.values()]
        group_names.append("(无)")
        self.group_combo = ttk.Combobox(self.dialog, values=group_names)
        self.group_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        if person:
            self.name_entry.insert(0, person.name)
            self.role_combo.set(person.role.value)
            group_name = groups.get(person.group_id, {}).name if person.group_id else "(无)"
            self.group_combo.set(group_name)
        
        ttk.Button(self.dialog, text="确定", command=self.ok).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self.dialog, text="取消", command=self.cancel).grid(row=3, column=1, padx=5, pady=10)
        
        self.dialog.columnconfigure(1, weight=1)
        
        parent.wait_window(self.dialog)
    
    def ok(self):
        name = self.name_entry.get().strip()
        role_text = self.role_combo.get()
        group_text = self.group_combo.get()
        
        if not name:
            messagebox.showwarning("提示", "请输入姓名")
            return
        
        if not role_text:
            messagebox.showwarning("提示", "请选择身份")
            return
        
        role = Role(role_text)
        
        if role == Role.GENERAL_MANAGER:
            existing_gm = next((p for p in self.people.values() if p.role == Role.GENERAL_MANAGER), None)
            if existing_gm and (not self.person or existing_gm.id != self.person.id):
                messagebox.showwarning("提示", "已存在总主管，不能再添加")
                return
        
        group_id = None
        group_name_to_create = None
        
        if group_text and group_text != "(无)":
            group = next((g for g in self.groups.values() if g.name == group_text), None)
            if group:
                group_id = group.id
            elif role == Role.TEAM_LEADER:
                group_name_to_create = group_text
            else:
                messagebox.showwarning("提示", f"组别'{group_text}'不存在，成员必须选择现有组别")
                return
        
        if role == Role.TEAM_LEADER:
            if not group_text or group_text == "(无)":
                messagebox.showwarning("提示", "组长必须分配到组")
                return
        
        if role == Role.MEMBER:
            if not group_text or group_text == "(无)":
                messagebox.showwarning("提示", "成员必须分配到组")
                return
        
        if self.person:
            person_id = self.person.id
        else:
            person_id = str(uuid.uuid4())
        
        if group_name_to_create:
            leader_id = person_id if role == Role.TEAM_LEADER else None
            new_group = Group(
                id=str(uuid.uuid4()),
                name=group_name_to_create,
                leader_id=leader_id,
                members=[]
            )
            self.groups[new_group.id] = new_group
            group_id = new_group.id
        
        self.result = Person(id=person_id, name=name, role=role, group_id=group_id)
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

class TierDialog:
    def __init__(self, parent, tier=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("编辑提成阶梯")
        self.dialog.geometry("300x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="下限金额（>=）：").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.min_entry = ttk.Entry(self.dialog)
        self.min_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="上限金额（<）：").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_entry = ttk.Entry(self.dialog)
        self.max_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(self.dialog, text="(空表示无上限)").grid(row=2, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(self.dialog, text="提成比例（%）：").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.rate_entry = ttk.Entry(self.dialog)
        self.rate_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="说明：业绩 >= 下限 且 < 上限").grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        if tier:
            self.min_entry.insert(0, str(tier.min_amount))
            if tier.max_amount:
                self.max_entry.insert(0, str(tier.max_amount))
            self.rate_entry.insert(0, str(tier.rate * 100))
        
        ttk.Button(self.dialog, text="确定", command=self.ok).grid(row=5, column=0, padx=5, pady=10)
        ttk.Button(self.dialog, text="取消", command=self.cancel).grid(row=5, column=1, padx=5, pady=10)
        
        self.dialog.columnconfigure(1, weight=1)
        
        parent.wait_window(self.dialog)
    
    def ok(self):
        try:
            min_amount = float(self.min_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "下限金额必须是数字")
            return
        
        max_text = self.max_entry.get().strip()
        max_amount = None
        if max_text:
            try:
                max_amount = float(max_text)
            except ValueError:
                messagebox.showwarning("提示", "上限金额必须是数字")
                return
            
            if max_amount <= min_amount:
                messagebox.showwarning("提示", "上限金额必须大于下限金额")
                return
        
        try:
            rate_percent = float(self.rate_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "提成比例必须是数字")
            return
        
        if rate_percent < 0 or rate_percent > 100:
            messagebox.showwarning("提示", "提成比例必须在0-100之间")
            return
        
        self.result = {
            "min_amount": min_amount,
            "max_amount": max_amount,
            "rate": rate_percent / 100
        }
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

class BonusDialog:
    def __init__(self, parent, bonus=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("编辑奖金阶梯")
        self.dialog.geometry("300x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="业绩阈值：").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.threshold_entry = ttk.Entry(self.dialog)
        self.threshold_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="奖金金额：").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(self.dialog)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(self.dialog, text="说明：业绩 >= 阈值 即获得奖金").grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        if bonus:
            self.threshold_entry.insert(0, str(bonus.threshold))
            self.amount_entry.insert(0, str(bonus.amount))
        
        ttk.Button(self.dialog, text="确定", command=self.ok).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self.dialog, text="取消", command=self.cancel).grid(row=3, column=1, padx=5, pady=10)
        
        self.dialog.columnconfigure(1, weight=1)
        
        parent.wait_window(self.dialog)
    
    def ok(self):
        try:
            threshold = float(self.threshold_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "业绩阈值必须是数字")
            return
        
        if threshold <= 0:
            messagebox.showwarning("提示", "业绩阈值必须大于0")
            return
        
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showwarning("提示", "奖金金额必须是数字")
            return
        
        if amount <= 0:
            messagebox.showwarning("提示", "奖金金额必须大于0")
            return
        
        self.result = {
            "threshold": threshold,
            "amount": amount
        }
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()
class TextImportDialog:
    def __init__(self, parent, people):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("粘贴文本导入业绩")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.people = people
        
        ttk.Label(self.dialog, text="请粘贴业绩文本（支持制表符分隔格式）").pack(padx=5, pady=5)
        ttk.Label(self.dialog, text="示例格式：部门\t小组\t姓名\t累计业绩\t核对").pack(padx=5)
        
        text_frame = ttk.Frame(self.dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = tk.Text(text_frame, height=20)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(self.dialog, text="识别解析", command=self.parse_text).pack(pady=5)
        
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
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)
        
        ttk.Label(self.dialog, text="提示：状态为'已匹配'的人员已有身份配置").pack(padx=5)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="确认导入", command=self.confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
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
                elif col.strip() in ["累计业绩", "业绩", "金额", "业绩金额"]:
                    performance_col_index = i
        
        if name_col_index is None:
            messagebox.showwarning("提示", "无法识别姓名列，请确保文本包含'姓名'列")
            return
        
        if performance_col_index is None:
            messagebox.showwarning("提示", "无法识别业绩列，请确保文本包含'累计业绩'或'业绩'列")
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
