import tkinter as tk
from tkinter import ttk
from src.repositories.config_repo import ConfigRepository
from src.repositories.excel_repo import ExcelRepository
from src.repositories.people_repo import PeopleRepository
from src.services.calculator import CommissionCalculator
from src.models.config import Config
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.ui.utils import configure_treeview_center, configure_treeview_grid
from src.ui.export_dialog import ExportDialog
from src.utils.logger import get_logger

class MainWindow:
    def __init__(self):
        self.logger = get_logger()
        self.logger.info("系统启动")
        
        self.root = tk.Tk()
        self.root.title("绩效提成计算系统")
        self.root.geometry("900x700")
        
        self._configure_styles()
        
        self.config_repo = ConfigRepository("config")
        self.excel_repo = ExcelRepository()
        self.people_repo = PeopleRepository("config")
        self.config = self.config_repo.load()
        self.logger.info("配置加载完成")
        
        self.calculator = CommissionCalculator(self.config)
        
        self.people = {}
        self.groups = {}
        self.performance_data = {}
        
        self._load_people_config()
        
        self._create_menu()
        self._create_notebook()
        self._create_status_bar()
    
    def _configure_styles(self):
        """配置全局样式"""
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Item", anchor=tk.CENTER)
        style.configure("Treeview.Heading", anchor=tk.CENTER)
    
    def _load_people_config(self):
        self.people, self.groups = self.people_repo.load()
        self.logger.info(f"加载人员配置: {len(self.people)}人, {len(self.groups)}组")
        
        fixed = False
        for person in self.people.values():
            if person.role == Role.MEMBER and person.group_id:
                group = self.groups.get(person.group_id)
                if group and person.id not in group.members:
                    group.add_member(person.id)
                    self.logger.info(f"自动修复: 添加成员'{person.name}'到组'{group.name}'")
                    fixed = True
        
        for group in self.groups.values():
            invalid_members = [m for m in group.members if m not in self.people]
            for m in invalid_members:
                group.remove_member(m)
                self.logger.info(f"自动修复: 从组'{group.name}'移除无效成员ID'{m}'")
                fixed = True
            
            for mid in group.members:
                person = self.people.get(mid)
                if person and person.group_id != group.id:
                    group.remove_member(mid)
                    self.logger.info(f"自动修复: 从组'{group.name}'移除不匹配成员'{person.name}'")
                    fixed = True
        
        if fixed:
            self.people_repo.save(self.people, self.groups)
            self.logger.info("已保存修复后的配置")
        
        for g in self.groups.values():
            leader = self.people.get(g.leader_id)
            leader_name = leader.name if leader else "无"
            member_names = [self.people.get(m).name if self.people.get(m) else f"(无效:{m})" for m in g.members]
            self.logger.debug(f"  组别[{g.name}]: 组长={leader_name}, 成员数={len(g.members)}, 成员={member_names}")
        
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
        configure_treeview_center(self.performance_tree)
        self.performance_tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.commission_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="粘贴文本导入", command=self.import_text_performance).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="计算提成", command=self.calculate_commission).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出结果", command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        result_frame = ttk.LabelFrame(self.commission_frame, text="提成结果", padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_tree = ttk.Treeview(result_frame, columns=("姓名", "提成点数", "个人提成", "团队提成", "管理提成", "奖金", "销冠奖金", "总计"), show="headings", height=8)
        self.result_tree.heading("姓名", text="姓名")
        self.result_tree.heading("提成点数", text="提成点数")
        self.result_tree.heading("个人提成", text="个人提成")
        self.result_tree.heading("团队提成", text="团队提成")
        self.result_tree.heading("管理提成", text="管理提成")
        self.result_tree.heading("奖金", text="奖金")
        self.result_tree.heading("销冠奖金", text="销冠奖金")
        self.result_tree.heading("总计", text="总计")
        self.result_tree.column("姓名", width=80)
        self.result_tree.column("提成点数", width=80)
        self.result_tree.column("个人提成", width=80)
        self.result_tree.column("团队提成", width=80)
        self.result_tree.column("管理提成", width=80)
        self.result_tree.column("奖金", width=80)
        self.result_tree.column("销冠奖金", width=80)
        self.result_tree.column("总计", width=80)
        configure_treeview_center(self.result_tree)
        self.result_tree.pack(fill=tk.BOTH, expand=True)
    
    def _create_people_tab(self):
        tree_frame = ttk.Frame(self.people_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.people_tree = ttk.Treeview(tree_frame, columns=("姓名", "身份", "组别", "管理组别"), show="headings", height=15)
        self.people_tree.heading("姓名", text="姓名")
        self.people_tree.heading("身份", text="身份")
        self.people_tree.heading("组别", text="组别")
        self.people_tree.heading("管理组别", text="管理组别")
        self.people_tree.column("姓名", width=150)
        self.people_tree.column("身份", width=100)
        self.people_tree.column("组别", width=100)
        self.people_tree.column("管理组别", width=150)
        configure_treeview_center(self.people_tree)
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
        ttk.Label(tip_frame, text="- 临时组长只能有一位").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 分主管需管理至少1个组").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 组长必须分配到组").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 成员必须分配到组").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 点击'保存配置'按钮才能生效").pack(anchor=tk.W)
        ttk.Label(tip_frame, text="- 配置保存后下次启动自动加载").pack(anchor=tk.W)
        
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
        
        def on_mousewheel(event):
            self.rules_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.rules_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
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
        configure_treeview_center(self.personal_tree)
        self.personal_tree.pack(fill=tk.X)
        
        ttk.Button(personal_frame, text="添加阶梯", command=lambda: self.add_tier("personal")).pack(side=tk.LEFT, padx=5)
        ttk.Button(personal_frame, text="编辑阶梯", command=lambda: self.edit_tier("personal")).pack(side=tk.LEFT, padx=5)
        ttk.Button(personal_frame, text="删除阶梯", command=lambda: self.delete_tier("personal")).pack(side=tk.LEFT, padx=5)
        
        team_frame = ttk.LabelFrame(rules_inner_frame, text="正式组长团队提成阶梯配置", padding="5")
        team_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.team_tree = ttk.Treeview(team_frame, columns=("下限", "上限", "提成比例"), show="headings", height=4)
        self.team_tree.heading("下限", text="下限")
        self.team_tree.heading("上限", text="上限")
        self.team_tree.heading("提成比例", text="提成比例")
        self.team_tree.column("下限", width=150)
        self.team_tree.column("上限", width=150)
        self.team_tree.column("提成比例", width=150)
        configure_treeview_center(self.team_tree)
        self.team_tree.pack(fill=tk.X)
        
        ttk.Button(team_frame, text="添加阶梯", command=lambda: self.add_tier("team")).pack(side=tk.LEFT, padx=5)
        ttk.Button(team_frame, text="编辑阶梯", command=lambda: self.edit_tier("team")).pack(side=tk.LEFT, padx=5)
        ttk.Button(team_frame, text="删除阶梯", command=lambda: self.delete_tier("team")).pack(side=tk.LEFT, padx=5)
        
        threshold_frame = ttk.Frame(team_frame)
        threshold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(threshold_frame, text="个人业绩达标线（元）：").pack(side=tk.LEFT)
        self.threshold_entry = ttk.Entry(threshold_frame, width=10)
        self.threshold_entry.insert(0, str(self.config.eligible_performance_threshold))
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(threshold_frame, text="（低于此业绩不计入团队提成）").pack(side=tk.LEFT)
        
        gm_frame = ttk.LabelFrame(rules_inner_frame, text="总主管提成配置", padding="5")
        gm_frame.pack(fill=tk.X, padx=5, pady=5)
        
        gm_threshold_frame = ttk.Frame(gm_frame)
        gm_threshold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gm_threshold_frame, text="总主管达标线（元）：").pack(side=tk.LEFT)
        self.gm_threshold_entry = ttk.Entry(gm_threshold_frame, width=10)
        self.gm_threshold_entry.insert(0, str(self.config.gm_eligible_threshold))
        self.gm_threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(gm_threshold_frame, text="（低于此业绩不计入总主管团队提成）").pack(side=tk.LEFT)
        
        self.gm_tree = ttk.Treeview(gm_frame, columns=("下限", "上限", "提成比例"), show="headings", height=2)
        self.gm_tree.heading("下限", text="下限")
        self.gm_tree.heading("上限", text="上限")
        self.gm_tree.heading("提成比例", text="提成比例")
        self.gm_tree.column("下限", width=150)
        self.gm_tree.column("上限", width=150)
        self.gm_tree.column("提成比例", width=150)
        configure_treeview_center(self.gm_tree)
        self.gm_tree.pack(fill=tk.X)
        
        ttk.Button(gm_frame, text="添加阶梯", command=lambda: self.add_tier("gm")).pack(side=tk.LEFT, padx=5)
        ttk.Button(gm_frame, text="编辑阶梯", command=lambda: self.edit_tier("gm")).pack(side=tk.LEFT, padx=5)
        ttk.Button(gm_frame, text="删除阶梯", command=lambda: self.delete_tier("gm")).pack(side=tk.LEFT, padx=5)
        
        temp_leader_frame = ttk.LabelFrame(rules_inner_frame, text="临时组长提成配置", padding="5")
        temp_leader_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tl_threshold_frame = ttk.Frame(temp_leader_frame)
        tl_threshold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(tl_threshold_frame, text="临时组长达标线（元）：").pack(side=tk.LEFT)
        self.temp_leader_threshold_entry = ttk.Entry(tl_threshold_frame, width=10)
        self.temp_leader_threshold_entry.insert(0, str(self.config.temp_leader_eligible_threshold))
        self.temp_leader_threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(tl_threshold_frame, text="（低于此业绩不计入临时组长团队提成）").pack(side=tk.LEFT)
        
        self.temp_leader_tree = ttk.Treeview(temp_leader_frame, columns=("下限", "上限", "提成比例"), show="headings", height=3)
        self.temp_leader_tree.heading("下限", text="下限")
        self.temp_leader_tree.heading("上限", text="上限")
        self.temp_leader_tree.heading("提成比例", text="提成比例")
        self.temp_leader_tree.column("下限", width=150)
        self.temp_leader_tree.column("上限", width=150)
        self.temp_leader_tree.column("提成比例", width=150)
        configure_treeview_center(self.temp_leader_tree)
        self.temp_leader_tree.pack(fill=tk.X)
        
        ttk.Button(temp_leader_frame, text="添加阶梯", command=lambda: self.add_tier("temp_leader")).pack(side=tk.LEFT, padx=5)
        ttk.Button(temp_leader_frame, text="编辑阶梯", command=lambda: self.edit_tier("temp_leader")).pack(side=tk.LEFT, padx=5)
        ttk.Button(temp_leader_frame, text="删除阶梯", command=lambda: self.delete_tier("temp_leader")).pack(side=tk.LEFT, padx=5)
        
        branch_manager_frame = ttk.LabelFrame(rules_inner_frame, text="分主管提成配置", padding="5")
        branch_manager_frame.pack(fill=tk.X, padx=5, pady=5)
        
        bm_threshold_frame = ttk.Frame(branch_manager_frame)
        bm_threshold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(bm_threshold_frame, text="分主管达标线（元）：").pack(side=tk.LEFT)
        self.branch_manager_threshold_entry = ttk.Entry(bm_threshold_frame, width=10)
        self.branch_manager_threshold_entry.insert(0, str(self.config.branch_manager_eligible_threshold))
        self.branch_manager_threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(bm_threshold_frame, text="（低于此业绩不计入分主管团队提成）").pack(side=tk.LEFT)
        
        self.branch_manager_tree = ttk.Treeview(branch_manager_frame, columns=("下限", "上限", "提成比例"), show="headings", height=2)
        self.branch_manager_tree.heading("下限", text="下限")
        self.branch_manager_tree.heading("上限", text="上限")
        self.branch_manager_tree.heading("提成比例", text="提成比例")
        self.branch_manager_tree.column("下限", width=150)
        self.branch_manager_tree.column("上限", width=150)
        self.branch_manager_tree.column("提成比例", width=150)
        configure_treeview_center(self.branch_manager_tree)
        self.branch_manager_tree.pack(fill=tk.X)
        
        ttk.Button(branch_manager_frame, text="添加阶梯", command=lambda: self.add_tier("branch_manager")).pack(side=tk.LEFT, padx=5)
        ttk.Button(branch_manager_frame, text="编辑阶梯", command=lambda: self.edit_tier("branch_manager")).pack(side=tk.LEFT, padx=5)
        ttk.Button(branch_manager_frame, text="删除阶梯", command=lambda: self.delete_tier("branch_manager")).pack(side=tk.LEFT, padx=5)
        
        management_frame = ttk.LabelFrame(rules_inner_frame, text="管理提成", padding="5")
        management_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(management_frame, text="每人管理提成金额（元）：").pack(side=tk.LEFT)
        self.management_entry = ttk.Entry(management_frame, width=10)
        self.management_entry.insert(0, str(self.config.management_bonus_per_person))
        self.management_entry.pack(side=tk.LEFT, padx=5)
        
        bonus_frame = ttk.LabelFrame(rules_inner_frame, text="高业绩奖金配置（达到阈值即获得奖金，不累加）", padding="5")
        bonus_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.bonus_tree = ttk.Treeview(bonus_frame, columns=("业绩阈值", "奖金金额"), show="headings", height=4)
        self.bonus_tree.heading("业绩阈值", text="业绩阈值")
        self.bonus_tree.heading("奖金金额", text="奖金金额")
        self.bonus_tree.column("业绩阈值", width=150)
        self.bonus_tree.column("奖金金额", width=150)
        configure_treeview_center(self.bonus_tree)
        self.bonus_tree.pack(fill=tk.X)
        
        ttk.Button(bonus_frame, text="添加奖金阶梯", command=self.add_bonus).pack(side=tk.LEFT, padx=5)
        ttk.Button(bonus_frame, text="编辑奖金阶梯", command=self.edit_bonus).pack(side=tk.LEFT, padx=5)
        ttk.Button(bonus_frame, text="删除奖金阶梯", command=self.delete_bonus).pack(side=tk.LEFT, padx=5)
        
        sales_champion_frame = ttk.LabelFrame(rules_inner_frame, text="销冠奖金配置", padding="5")
        sales_champion_frame.pack(fill=tk.X, padx=5, pady=5)
        
        sc_threshold_frame = ttk.Frame(sales_champion_frame)
        sc_threshold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(sc_threshold_frame, text="销冠阈值（元）：").pack(side=tk.LEFT)
        self.sales_champion_threshold_entry = ttk.Entry(sc_threshold_frame, width=10)
        self.sales_champion_threshold_entry.insert(0, str(self.config.sales_champion_threshold))
        self.sales_champion_threshold_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(sc_threshold_frame, text="（业绩最高且>=阈值者获得销冠奖金）").pack(side=tk.LEFT)
        
        sc_bonus_frame = ttk.Frame(sales_champion_frame)
        sc_bonus_frame.pack(fill=tk.X, pady=5)
        ttk.Label(sc_bonus_frame, text="销冠奖金（元）：").pack(side=tk.LEFT)
        self.sales_champion_bonus_entry = ttk.Entry(sc_bonus_frame, width=10)
        self.sales_champion_bonus_entry.insert(0, str(self.config.sales_champion_bonus))
        self.sales_champion_bonus_entry.pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(rules_inner_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="保存配置", command=self.save_rules_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置默认", command=self.reset_rules).pack(side=tk.LEFT, padx=5)
        
        self._refresh_rules_trees()
    
    def _create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("请粘贴文本导入业绩数据开始计算")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def import_performance(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(title="选择业绩Excel文件", filetypes=[("Excel文件", "*.xlsx *.xls")])
        if file_path:
            self.logger.info(f"导入Excel文件: {file_path}")
            try:
                self.performance_data = self.excel_repo.import_performance_data(file_path)
                self._update_performance_tree()
                self.status_var.set(f"已导入{len(self.performance_data)}条业绩数据")
                self.logger.info(f"成功导入{len(self.performance_data)}条业绩数据")
            except ValueError as e:
                self.logger.error(f"导入失败: {str(e)}")
                messagebox.showerror("导入失败", str(e))
    
    def import_text_performance(self):
        from src.ui.text_import_dialog import TextImportDialog
        dialog = TextImportDialog(self.root, self.people)
        if dialog.result:
            self.performance_data = dialog.result
            self.logger.info(f"粘贴文本导入{len(self.performance_data)}条业绩数据")
            self._update_performance_tree()
            self.status_var.set(f"已导入{len(self.performance_data)}条业绩数据")
    
    def _update_performance_tree(self):
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)
        
        for name, performance in self.performance_data.items():
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                group = self.groups.get(person.group_id)
                group_name = group.name if group else ""
                self.performance_tree.insert("", tk.END, values=(name, performance, person.role.value, group_name))
            else:
                self.performance_tree.insert("", tk.END, values=(name, performance, "", ""))
    
    def calculate_commission(self):
        from tkinter import messagebox
        
        if not self.performance_data:
            self.logger.warning("未导入业绩数据")
            messagebox.showwarning("提示", "请先导入业绩数据")
            return
        
        unconfigured = []
        for name in self.performance_data.keys():
            if not any(p.name == name for p in self.people.values()):
                unconfigured.append(name)
        
        if unconfigured:
            self.logger.warning(f"人员配置不完整: {', '.join(unconfigured)}")
            messagebox.showwarning("人员配置不完整", f"以下人员缺少身份配置：{', '.join(unconfigured)}，请先在人员管理中配置")
            return
        
        self.logger.info("开始计算提成")
        
        for name, performance in self.performance_data.items():
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                person.performance = performance
        
        self.calculator.set_people(self.people)
        self.calculator.set_groups(self.groups)
        
        results = self.calculator.calculate_all()
        
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        for name, performance in self.performance_data.items():
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                result = results.get(person.id)
                if result:
                    self.result_tree.insert("", tk.END, values=(
                        name,
                        f"{result.commission_rate*100:.1f}%",
                        result.personal_commission,
                        result.team_commission,
                        result.management_bonus,
                        result.high_performance_bonus,
                        result.sales_champion_bonus,
                        result.total
                    ))
        
        self.status_var.set(f"已计算{len(self.performance_data)}人提成")
        self.logger.info(f"完成{len(self.performance_data)}人提成计算")
    
    def export_results(self):
        from tkinter import filedialog, messagebox
        
        if not self.result_tree.get_children():
            messagebox.showwarning("提示", "请先计算提成")
            return
        
        dialog = ExportDialog(self.root, self.people, "config")
        if not dialog.result:
            return
        
        file_path = filedialog.asksaveasfilename(title="保存结果Excel文件", defaultextension=".xlsx", filetypes=[("Excel文件", "*.xlsx")])
        if not file_path:
            return
        
        if dialog.order:
            results = self._build_results_by_order(dialog.order)
        else:
            results = self._build_results_from_tree()
        
        self.excel_repo.export_results(results, file_path)
        messagebox.showinfo("导出成功", f"结果已保存到 {file_path}")
    
    def _build_results_by_order(self, order):
        results = []
        result_map = {}
        for item in self.result_tree.get_children():
            values = self.result_tree.item(item)["values"]
            name = values[0]
            result_map[name] = values
        
        for name in order:
            if name in result_map:
                values = result_map[name]
                person = next((p for p in self.people.values() if p.name == name), None)
                if person:
                    group = self.groups.get(person.group_id)
                    group_name = group.name if group else ""
                    results.append({
                        "姓名": name,
                        "业绩": person.performance,
                        "身份": person.role.value,
                        "组别": group_name,
                        "提成点数": values[1],
                        "个人提成": values[2],
                        "团队提成": values[3],
                        "管理提成": values[4],
                        "高业绩奖金": values[5],
                        "销冠奖金": values[6],
                        "总提成": values[7]
                    })
            else:
                results.append({
                    "姓名": name,
                    "业绩": 0,
                    "身份": "",
                    "组别": "",
                    "提成点数": "0%",
                    "个人提成": 0,
                    "团队提成": 0,
                    "管理提成": 0,
                    "高业绩奖金": 0,
                    "销冠奖金": 0,
                    "总提成": 0
                })
        return results
    
    def _build_results_from_tree(self):
        results = []
        for item in self.result_tree.get_children():
            values = self.result_tree.item(item)["values"]
            person = next((p for p in self.people.values() if p.name == values[0]), None)
            if person:
                group = self.groups.get(person.group_id)
                group_name = group.name if group else ""
                results.append({
                    "姓名": values[0],
                    "业绩": person.performance,
                    "身份": person.role.value,
                    "组别": group_name,
                    "提成点数": values[1],
                    "个人提成": values[2],
                    "团队提成": values[3],
                    "管理提成": values[4],
                    "高业绩奖金": values[5],
                    "销冠奖金": values[6],
                    "总提成": values[7]
                })
        return results
    
    def add_person(self):
        from src.ui.dialogs import PersonDialog
        dialog = PersonDialog(self.root, self.people, self.groups)
        if dialog.result:
            person = dialog.result
            self.people[person.id] = person
            self.logger.info(f"添加人员: {person.name}, 身份={person.role.value}, 组别={self.groups.get(person.group_id).name if self.groups.get(person.group_id) else '无'}")
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
            old_group = self.groups.get(person.group_id)
            old_group_name = old_group.name if old_group else "无"
            dialog = PersonDialog(self.root, self.people, self.groups, person)
            if dialog.result:
                new_person = dialog.result
                new_group = self.groups.get(new_person.group_id)
                new_group_name = new_group.name if new_group else "无"
                self.logger.info(f"编辑人员: {new_person.name}, 身份={new_person.role.value}, 组别从'{old_group_name}'改为'{new_group_name}'")
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
            person = next((p for p in self.people.values() if p.name == name), None)
            if person:
                if person.group_id:
                    group = self.groups.get(person.group_id)
                    if group and person.id in group.members:
                        group.remove_member(person.id)
                        self.logger.debug(f"  从组'{group.name}'移除成员'{name}'")
                del self.people[person.id]
                self.logger.info(f"删除人员: {name}")
                self._update_people_tree()
    
    def save_people_config(self):
        from tkinter import messagebox
        
        self.people_repo.save(self.people, self.groups)
        self.logger.info(f"保存人员配置: {len(self.people)}人, {len(self.groups)}组")
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
                group = self.groups.get(person.group_id)
                group_name = group.name if group else ""
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
            group = self.groups.get(person.group_id)
            group_name = group.name if group else ""
            managed_names = [self.groups.get(gid).name for gid in person.managed_groups if self.groups.get(gid)]
            managed_str = ", ".join(managed_names) if managed_names else ""
            self.people_tree.insert("", tk.END, values=(person.name, person.role.value, group_name, managed_str))
    
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
        
        for item in self.gm_tree.get_children():
            self.gm_tree.delete(item)
        for tier in self.config.gm_commission.tiers:
            max_text = str(tier.max_amount) if tier.max_amount else "(空)"
            self.gm_tree.insert("", tk.END, values=(tier.min_amount, max_text, f"{tier.rate*100}%"))
        
        for item in self.temp_leader_tree.get_children():
            self.temp_leader_tree.delete(item)
        for tier in self.config.temp_leader_commission.tiers:
            max_text = str(tier.max_amount) if tier.max_amount else "(空)"
            self.temp_leader_tree.insert("", tk.END, values=(tier.min_amount, max_text, f"{tier.rate*100}%"))
        
        for item in self.branch_manager_tree.get_children():
            self.branch_manager_tree.delete(item)
        for tier in self.config.branch_manager_commission.tiers:
            max_text = str(tier.max_amount) if tier.max_amount else "(空)"
            self.branch_manager_tree.insert("", tk.END, values=(tier.min_amount, max_text, f"{tier.rate*100}%"))
        
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
            elif tier_type == "team":
                self.config.team_commission.tiers.append(tier)
            elif tier_type == "gm":
                self.config.gm_commission.tiers.append(tier)
            elif tier_type == "temp_leader":
                self.config.temp_leader_commission.tiers.append(tier)
            elif tier_type == "branch_manager":
                self.config.branch_manager_commission.tiers.append(tier)
            self._refresh_rules_trees()
    
    def edit_tier(self, tier_type):
        from tkinter import messagebox
        from src.ui.dialogs import TierDialog
        
        if tier_type == "personal":
            tree = self.personal_tree
        elif tier_type == "team":
            tree = self.team_tree
        elif tier_type == "gm":
            tree = self.gm_tree
        elif tier_type == "temp_leader":
            tree = self.temp_leader_tree
        elif tier_type == "branch_manager":
            tree = self.branch_manager_tree
        else:
            return
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择阶梯")
            return
        
        index = tree.index(selected[0])
        if tier_type == "personal":
            tiers = self.config.personal_commission.tiers
        elif tier_type == "team":
            tiers = self.config.team_commission.tiers
        elif tier_type == "gm":
            tiers = self.config.gm_commission.tiers
        elif tier_type == "temp_leader":
            tiers = self.config.temp_leader_commission.tiers
        elif tier_type == "branch_manager":
            tiers = self.config.branch_manager_commission.tiers
        else:
            return
        tier = tiers[index]
        
        dialog = TierDialog(self.root, tier)
        if dialog.result:
            tier.min_amount = dialog.result["min_amount"]
            tier.max_amount = dialog.result["max_amount"]
            tier.rate = dialog.result["rate"]
            self._refresh_rules_trees()
    
    def delete_tier(self, tier_type):
        from tkinter import messagebox
        
        if tier_type == "personal":
            tree = self.personal_tree
        elif tier_type == "team":
            tree = self.team_tree
        elif tier_type == "gm":
            tree = self.gm_tree
        elif tier_type == "temp_leader":
            tree = self.temp_leader_tree
        elif tier_type == "branch_manager":
            tree = self.branch_manager_tree
        else:
            return
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择阶梯")
            return
        
        if messagebox.askyesno("确认删除", "确定删除此阶梯吗？"):
            index = tree.index(selected[0])
            if tier_type == "personal":
                tiers = self.config.personal_commission.tiers
            elif tier_type == "team":
                tiers = self.config.team_commission.tiers
            elif tier_type == "gm":
                tiers = self.config.gm_commission.tiers
            elif tier_type == "temp_leader":
                tiers = self.config.temp_leader_commission.tiers
            elif tier_type == "branch_manager":
                tiers = self.config.branch_manager_commission.tiers
            else:
                return
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
        
        try:
            self.config.gm_eligible_threshold = float(self.gm_threshold_entry.get())
        except ValueError:
            pass
        
        try:
            self.config.temp_leader_eligible_threshold = float(self.temp_leader_threshold_entry.get())
        except ValueError:
            pass
        
        try:
            self.config.branch_manager_eligible_threshold = float(self.branch_manager_threshold_entry.get())
        except ValueError:
            pass
        
        try:
            self.config.sales_champion_threshold = float(self.sales_champion_threshold_entry.get())
        except ValueError:
            pass
        
        try:
            self.config.sales_champion_bonus = float(self.sales_champion_bonus_entry.get())
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
            self.gm_threshold_entry.delete(0, tk.END)
            self.gm_threshold_entry.insert(0, str(self.config.gm_eligible_threshold))
            self.temp_leader_threshold_entry.delete(0, tk.END)
            self.temp_leader_threshold_entry.insert(0, str(self.config.temp_leader_eligible_threshold))
            self.branch_manager_threshold_entry.delete(0, tk.END)
            self.branch_manager_threshold_entry.insert(0, str(self.config.branch_manager_eligible_threshold))
            self.sales_champion_threshold_entry.delete(0, tk.END)
            self.sales_champion_threshold_entry.insert(0, str(self.config.sales_champion_threshold))
            self.sales_champion_bonus_entry.delete(0, tk.END)
            self.sales_champion_bonus_entry.insert(0, str(self.config.sales_champion_bonus))
            self._refresh_rules_trees()
    
    def show_help(self):
        from tkinter import messagebox
        help_text = """
使用说明：

1. 导入业绩：点击"粘贴文本导入"，粘贴文本（包含姓名和业绩列）
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