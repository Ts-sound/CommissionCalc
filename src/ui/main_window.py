import tkinter as tk
from tkinter import ttk
from src.repositories.config_repo import ConfigRepository
from src.repositories.excel_repo import ExcelRepository
from src.repositories.people_repo import PeopleRepository
from src.services.calculator import CommissionCalculator
from src.models.config import Config
from src.models.person import Person
from src.models.group import Group

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("绩效提成计算系统")
        self.root.geometry("900x700")
        
        self.config_repo = ConfigRepository("config")
        self.excel_repo = ExcelRepository()
        self.people_repo = PeopleRepository("config")
        self.config = self.config_repo.load()
        self.calculator = CommissionCalculator(self.config)
        
        self.people = {}
        self.groups = {}
        self.performance_data = {}
        
        self._load_people_config()
        
        self._create_menu()
        self._create_notebook()
        self._create_status_bar()
    
    def _load_people_config(self):
        self.people, self.groups = self.people_repo.load()
        self.calculator.set_people(self.people)
        self.calculator.set_groups(self.groups)
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="导入业绩", command=self.import_performance)
        file_menu.add_command(label="导出结果", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        menubar.add_cascade(label="文件", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.commission_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.commission_frame, text="提成计算")
        self._create_commission_tab()
        
        self.people_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.people_frame, text="人员管理")
        self._create_people_tab()
        
        self.rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_frame, text="规则配置")
        self._create_rules_tab()
    
    def _create_commission_tab(self):
        performance_frame = ttk.LabelFrame(self.commission_frame, text="业绩数据", padding="5")
        performance_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.performance_tree = ttk.Treeview(performance_frame, columns=("姓名", "业绩", "身份", "组别"), show="headings", height=8)
        self.performance_tree.heading("姓名", text="姓名")
        self.performance_tree.heading("业绩", text="业绩")
        self.performance_tree.heading("身份", text="身份")
        self.performance_tree.heading("组别", text="组别")
        self.performance_tree.column("姓名", width=150)
        self.performance_tree.column("业绩", width=150)
        self.performance_tree.column("身份", width=150)
        self.performance_tree.column("组别", width=150)
        self.performance_tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.commission_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="导入Excel", command=self.import_performance).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="粘贴文本", command=self.import_text_performance).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="计算提成", command=self.calculate_commission).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出结果", command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        result_frame = ttk.LabelFrame(self.commission_frame, text="提成结果", padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_tree = ttk.Treeview(result_frame, columns=("姓名", "个人提成", "团队提成", "管理提成", "奖金", "总计"), show="headings", height=8)
        self.result_tree.heading("姓名", text="姓名")
        self.result_tree.heading("个人提成", text="个人提成")
        self.result_tree.heading("团队提成", text="团队提成")
        self.result_tree.heading("管理提成", text="管理提成")
        self.result_tree.heading("奖金", text="奖金")
        self.result_tree.heading("总计", text="总计")
        self.result_tree.column("姓名", width=100)
        self.result_tree.column("个人提成", width=100)
        self.result_tree.column("团队提成", width=100)
        self.result_tree.column("管理提成", width=100)
        self.result_tree.column("奖金", width=100)
        self.result_tree.column("总计", width=100)
        self.result_tree.pack(fill=tk.BOTH, expand=True)
    
    def _create_people_tab(self):
        tree_frame = ttk.Frame(self.people_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.people_tree = ttk.Treeview(tree_frame, columns=("姓名", "身份", "组别"), show="headings", height=15)
        self.people_tree.heading("姓名", text="姓名")
        self.people_tree.heading("身份", text="身份")
        self.people_tree.heading("组别", text="组别")
        self.people_tree.column("姓名", width=200)
        self.people_tree.column("身份", width=200)
        self.people_tree.column("组别", width=200)
        self.people_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.people_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.people_tree.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(self.people_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="添加人员", command=self.add_person).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑人员", command=self.edit_person).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除人员", command=self.delete_person).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存配置", command=self.save_people_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出Excel", command=self.export_people_to_excel).pack(side=tk.LEFT, padx=5)
        
        tip_frame = ttk.LabelFrame(self.people_frame, text="提示", padding="5")
        tip_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(tip_frame, text="- 总主管只能有一位").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 组长必须分配到组").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 成员必须分配到组").pack(anchor=tk.W)
        
        self._update_people_tree()
    
    def _create_rules_tab(self):
        self.rules_canvas = tk.Canvas(self.rules_frame)
        scrollbar = ttk.Scrollbar(self.rules_frame, orient=tk.VERTICAL, command=self.rules_canvas.yview)
        self.rules_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.rules_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        rules_inner_frame = ttk.Frame(self.rules_canvas)
        self.rules_canvas.create_window((0, 0), window=rules_inner_frame, anchor=tk.NW)
        rules_inner_frame.bind("<Configure>", lambda e: self.rules_canvas.configure(scrollregion=self.rules_canvas.bbox("all")))
        
        personal_frame = ttk.LabelFrame(rules_inner_frame, text="个人提成阶梯配置", padding="5")
        personal_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(personal_frame, text="说明：范围 <=业绩< 上限，上限为空表示无上限").pack(anchor=tk.W)
        
        self.personal_tree = ttk.Treeview(personal_frame, columns=("下限", "上限", "提成比例"), show="headings", height=4)
        self.personal_tree.heading("下限", text="下限")
        self.personal_tree.heading("上限", text="上限")
        self.personal_tree.heading("提成比例", text="提成比例")
        self.personal_tree.column("下限", width=150)
        self.personal_tree.column("上限", width=150)
        self.personal_tree.column("提成比例", width=150)
        self.personal_tree.pack(fill=tk.X)
        
        ttk.Button(personal_frame, text="添加阶梯", command=lambda: self.add_tier("personal")).pack(side=tk.LEFT, padx=5)
        ttk.Button(personal_frame, text="编辑阶梯", command=lambda: self.edit_tier("personal")).pack(side=tk.LEFT, padx=5)
        ttk.Button(personal_frame, text="删除阶梯", command=lambda: self.delete_tier("personal")).pack(side=tk.LEFT, padx=5)
        
        team_frame = ttk.LabelFrame(rules_inner_frame, text="团队提成阶梯配置", padding="5")
        team_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.team_tree = ttk.Treeview(team_frame, columns=("下限", "上限", "提成比例"), show="headings", height=4)
        self.team_tree.heading("下限", text="下限")
        self.team_tree.heading("上限", text="上限")
        self.team_tree.heading("提成比例", text="提成比例")
        self.team_tree.column("下限", width=150)
        self.team_tree.column("上限", width=150)
        self.team_tree.column("提成比例", width=150)
        self.team_tree.pack(fill=tk.X)
        
        ttk.Button(team_frame, text="添加阶梯", command=lambda: self.add_tier("team")).pack(side=tk.LEFT, padx=5)
        ttk.Button(team_frame, text="编辑阶梯", command=lambda: self.edit_tier("team")).pack(side=tk.LEFT, padx=5)
        ttk.Button(team_frame, text="删除阶梯", command=lambda: self.delete_tier("team")).pack(side=tk.LEFT, padx=5)
        
        management_frame = ttk.LabelFrame(rules_inner_frame, text="管理提成", padding="5")
        management_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(management_frame, text="每人管理提成金额（元）：").pack(side=tk.LEFT)
        self.management_entry = ttk.Entry(management_frame, width=10)
        self.management_entry.insert(0, str(self.config.management_bonus_per_person))
        self.management_entry.pack(side=tk.LEFT, padx=5)
        
        threshold_frame = ttk.LabelFrame(rules_inner_frame, text="团队业绩达标线", padding="5")
        threshold_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(threshold_frame, text="个人业绩达标线（元）：").pack(side=tk.LEFT)
        self.threshold_entry = ttk.Entry(threshold_frame, width=10)
        self.threshold_entry.insert(0, str(self.config.eligible_performance_threshold))
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(threshold_frame, text="（低于此业绩不计入团队提成）").pack(side=tk.LEFT)
        
        bonus_frame = ttk.LabelFrame(rules_inner_frame, text="高业绩奖金配置（达到阈值即获得奖金，可累加）", padding="5")
        bonus_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.bonus_tree = ttk.Treeview(bonus_frame, columns=("业绩阈值", "奖金金额"), show="headings", height=4)
        self.bonus_tree.heading("业绩阈值", text="业绩阈值")
        self.bonus_tree.heading("奖金金额", text="奖金金额")
        self.bonus_tree.column("业绩阈值", width=150)
        self.bonus_tree.column("奖金金额", width=150)
        self.bonus_tree.pack(fill=tk.X)
        
        ttk.Button(bonus_frame, text="添加奖金阶梯", command=self.add_bonus).pack(side=tk.LEFT, padx=5)
        ttk.Button(bonus_frame, text="编辑奖金阶梯", command=self.edit_bonus).pack(side=tk.LEFT, padx=5)
        ttk.Button(bonus_frame, text="删除奖金阶梯", command=self.delete_bonus).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(rules_inner_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="保存配置", command=self.save_rules_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置默认", command=self.reset_rules).pack(side=tk.LEFT, padx=5)
        
        self._refresh_rules_trees()
    
    def _create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("请导入Excel业绩文件开始计算")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def import_performance(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(title="选择业绩Excel文件", filetypes=[("Excel文件", "*.xlsx *.xls")])
        if file_path:
            try:
                self.performance_data = self.excel_repo.import_performance_data(file_path)
                self._update_performance_tree()
                self.status_var.set(f"已导入{len(self.performance_data)}条业绩数据")
            except ValueError as e:
                messagebox.showerror("导入失败", str(e))
    
    def import_text_performance(self):
        from src.ui.text_import_dialog import TextImportDialog
        dialog = TextImportDialog(self.root, self.people)
        if dialog.result:
            self.performance_data = dialog.result
            self._update_performance_tree()
            self.status_var.set(f"已导入{len(self.performance_data)}条业绩数据")
    
    def _update_performance_tree(self):
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)
        
        for name, performance in self.performance_data.items():
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                group_name = self.groups.get(person.group_id, {}).name if person.group_id else ""
                self.performance_tree.insert("", tk.END, values=(name, performance, person.role.value, group_name))
            else:
                self.performance_tree.insert("", tk.END, values=(name, performance, "", ""))
    
    def calculate_commission(self):
        from tkinter import messagebox
        
        if not self.performance_data:
            messagebox.showwarning("提示", "请先导入业绩数据")
            return
        
        unconfigured = []
        for name in self.performance_data.keys():
            if not any(p.name == name for p in self.people.values()):
                unconfigured.append(name)
        
        if unconfigured:
            messagebox.showwarning("人员配置不完整", f"以下人员缺少身份配置：{', '.join(unconfigured)}，请先在人员管理中配置")
            return
        
        self.calculator.set_people(self.people)
        self.calculator.set_groups(self.groups)
        
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        for name, performance in self.performance_data.items():
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                person.performance = performance
                result = self.calculator.calculate_person(person)
                self.result_tree.insert("", tk.END, values=(
                    name,
                    result.personal_commission,
                    result.team_commission,
                    result.management_bonus,
                    result.high_performance_bonus,
                    result.total
                ))
        
        self.status_var.set(f"已计算{len(self.performance_data)}人提成")
    
    def export_results(self):
        from tkinter import filedialog, messagebox
        
        if not self.result_tree.get_children():
            messagebox.showwarning("提示", "请先计算提成")
            return
        
        file_path = filedialog.asksaveasfilename(title="保存结果Excel文件", defaultextension=".xlsx", filetypes=[("Excel文件", "*.xlsx")])
        if file_path:
            results = []
            for item in self.result_tree.get_children():
                values = self.result_tree.item(item)["values"]
                person = next((p for p in self.people.values() if p.name == values[0]), None)
                if person:
                    group_name = self.groups.get(person.group_id, {}).name if person.group_id else ""
                    results.append({
                        "姓名": values[0],
                        "业绩": person.performance,
                        "身份": person.role.value,
                        "组别": group_name,
                        "个人提成": values[1],
                        "团队提成": values[2],
                        "管理提成": values[3],
                        "高业绩奖金": values[4],
                        "总提成": values[5]
                    })
            
            self.excel_repo.export_results(results, file_path)
            messagebox.showinfo("导出成功", f"结果已保存到 {file_path}")
    
    def add_person(self):
        from src.ui.dialogs import PersonDialog
        dialog = PersonDialog(self.root, self.people, self.groups)
        if dialog.result:
            person = dialog.result
            self.people[person.id] = person
            self._update_people_tree()
    
    def edit_person(self):
        from tkinter import messagebox
        from src.ui.dialogs import PersonDialog
        
        selected = self.people_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择人员")
            return
        
        item = selected[0]
        name = self.people_tree.item(item)["values"][0]
        person = next((p for p in self.people.values() if p.name == name), None)
        
        if person:
            dialog = PersonDialog(self.root, self.people, self.groups, person)
            if dialog.result:
                self.people[person.id] = dialog.result
                self._update_people_tree()
    
    def delete_person(self):
        from tkinter import messagebox
        
        selected = self.people_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择人员")
            return
        
        item = selected[0]
        name = self.people_tree.item(item)["values"][0]
        
        if messagebox.askyesno("确认删除", f"确定删除人员{name}吗？"):
            person_id = next((p.id for p in self.people.values() if p.name == name), None)
            if person_id:
                del self.people[person_id]
                self._update_people_tree()
    
    def save_people_config(self):
        from tkinter import messagebox
        
        self.people_repo.save(self.people, self.groups)
        self.calculator.set_people(self.people)
        self.calculator.set_groups(self.groups)
        messagebox.showinfo("保存成功", "人员配置已保存")
    
    def export_people_to_excel(self):
        from tkinter import filedialog, messagebox
        import pandas as pd
        
        file_path = filedialog.asksaveasfilename(
            title="保存人员配置Excel文件",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        
        if file_path:
            data = []
            for person in self.people.values():
                group_name = self.groups.get(person.group_id, {}).name if person.group_id else ""
                data.append({
                    "姓名": person.name,
                    "身份": person.role.value,
                    "组别": group_name
                })
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("导出成功", f"人员配置已导出到 {file_path}")
    
    def _update_people_tree(self):
        for item in self.people_tree.get_children():
            self.people_tree.delete(item)
        
        for person in self.people.values():
            group_name = self.groups.get(person.group_id, {}).name if person.group_id else ""
            self.people_tree.insert("", tk.END, values=(person.name, person.role.value, group_name))
    
    def _refresh_rules_trees(self):
        for item in self.personal_tree.get_children():
            self.personal_tree.delete(item)
        for tier in self.config.personal_commission.tiers:
            max_text = str(tier.max_amount) if tier.max_amount else "(空)"
            self.personal_tree.insert("", tk.END, values=(tier.min_amount, max_text, f"{tier.rate*100}%"))
        
        for item in self.team_tree.get_children():
            self.team_tree.delete(item)
        for tier in self.config.team_commission.tiers:
            max_text = str(tier.max_amount) if tier.max_amount else "(空)"
            self.team_tree.insert("", tk.END, values=(tier.min_amount, max_text, f"{tier.rate*100}%"))
        
        for item in self.bonus_tree.get_children():
            self.bonus_tree.delete(item)
        for bonus in self.config.high_performance_bonuses:
            self.bonus_tree.insert("", tk.END, values=(bonus.threshold, bonus.amount))
    
    def add_tier(self, tier_type):
        from src.ui.dialogs import TierDialog
        dialog = TierDialog(self.root)
        if dialog.result:
            from src.models.commission import Tier
            tier = Tier(min_amount=dialog.result["min_amount"], max_amount=dialog.result["max_amount"], rate=dialog.result["rate"])
            if tier_type == "personal":
                self.config.personal_commission.tiers.append(tier)
            else:
                self.config.team_commission.tiers.append(tier)
            self._refresh_rules_trees()
    
    def edit_tier(self, tier_type):
        from tkinter import messagebox
        from src.ui.dialogs import TierDialog
        
        tree = self.personal_tree if tier_type == "personal" else self.team_tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择阶梯")
            return
        
        index = tree.index(selected[0])
        tiers = self.config.personal_commission.tiers if tier_type == "personal" else self.config.team_commission.tiers
        tier = tiers[index]
        
        dialog = TierDialog(self.root, tier)
        if dialog.result:
            tier.min_amount = dialog.result["min_amount"]
            tier.max_amount = dialog.result["max_amount"]
            tier.rate = dialog.result["rate"]
            self._refresh_rules_trees()
    
    def delete_tier(self, tier_type):
        from tkinter import messagebox
        
        tree = self.personal_tree if tier_type == "personal" else self.team_tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择阶梯")
            return
        
        if messagebox.askyesno("确认删除", "确定删除此阶梯吗？"):
            index = tree.index(selected[0])
            tiers = self.config.personal_commission.tiers if tier_type == "personal" else self.config.team_commission.tiers
            tiers.pop(index)
            self._refresh_rules_trees()
    
    def add_bonus(self):
        from src.ui.dialogs import BonusDialog
        dialog = BonusDialog(self.root)
        if dialog.result:
            from src.models.commission import Bonus
            bonus = Bonus(threshold=dialog.result["threshold"], amount=dialog.result["amount"])
            self.config.high_performance_bonuses.append(bonus)
            self._refresh_rules_trees()
    
    def edit_bonus(self):
        from tkinter import messagebox
        from src.ui.dialogs import BonusDialog
        
        selected = self.bonus_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择奖金阶梯")
            return
        
        index = self.bonus_tree.index(selected[0])
        bonus = self.config.high_performance_bonuses[index]
        
        dialog = BonusDialog(self.root, bonus)
        if dialog.result:
            bonus.threshold = dialog.result["threshold"]
            bonus.amount = dialog.result["amount"]
            self._refresh_rules_trees()
    
    def delete_bonus(self):
        from tkinter import messagebox
        
        selected = self.bonus_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择奖金阶梯")
            return
        
        if messagebox.askyesno("确认删除", "确定删除此奖金阶梯吗？"):
            index = self.bonus_tree.index(selected[0])
            self.config.high_performance_bonuses.pop(index)
            self._refresh_rules_trees()
    
    def save_rules_config(self):
        from tkinter import messagebox
        
        try:
            self.config.management_bonus_per_person = float(self.management_entry.get())
        except ValueError:
            pass
        
        try:
            self.config.eligible_performance_threshold = float(self.threshold_entry.get())
        except ValueError:
            pass
        
        self.config_repo.save(self.config)
        self.calculator.config = self.config
        messagebox.showinfo("保存成功", "提成规则配置已保存")
    
    def reset_rules(self):
        from tkinter import messagebox
        
        if messagebox.askyesno("确认重置", "确定重置为默认配置吗？"):
            self.config = Config.default()
            self.management_entry.delete(0, tk.END)
            self.management_entry.insert(0, str(self.config.management_bonus_per_person))
            self.threshold_entry.delete(0, tk.END)
            self.threshold_entry.insert(0, str(self.config.eligible_performance_threshold))
            self._refresh_rules_trees()
    
    def show_help(self):
        from tkinter import messagebox
        help_text = """
使用说明：

1. 导入业绩：点击"导入业绩"按钮，选择Excel文件（包含姓名和业绩列）
2. 配置人员：在"人员管理"标签页中添加人员，设置身份和组别
3. 计算提成：点击"计算提成"按钮，系统自动计算所有人员提成
4. 导出结果：点击"导出结果"按钮，导出提成明细到Excel文件

提成规则可在"规则配置"标签页中修改。
"""
        messagebox.showinfo("使用说明", help_text)
    
    def show_about(self):
        from tkinter import messagebox
        messagebox.showinfo("关于", "CommissionCalc v1.0\n绩效提成计算系统\n基于Python + Tkinter开发")
    
    def run(self):
        self.root.mainloop()