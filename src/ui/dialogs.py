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
        
        if role == Role.MEMBER and group_id:
            group = self.groups.get(group_id)
            if group and person_id not in group.members:
                group.add_member(person_id)
        
        if self.person and self.person.role == Role.MEMBER and self.person.group_id != group_id:
            old_group = self.groups.get(self.person.group_id)
            if old_group and person_id in old_group.members:
                old_group.remove_member(person_id)
        
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
