# CommissionCalc

一款基于 Python 开发的绩效提成自动计算工具。

## 功能特性

- 粘贴文本导入业绩数据（支持制表符分隔格式）
- 可视化人员配置管理
- 可配置的提成规则设置
- 自动计算多种提成类型
- 详细的提成明细报表导出（Excel）
- 自动修复历史配置数据
- 详细计算日志便于排查问题

## 提成计算规则

### 个人业绩提成
- 0-3000元: 0%
- 3000元以上: 20%（全额计算）

### 团队业绩提成（组长/总主管）
- 只累加达标业绩（>=达标线，默认3000元）
- 包含组长/总主管自己的业绩
- 0-10000元: 0%
- 10000-50000元: 10%
- 50000元以上: 20%（全额计算）
- 达标线可在规则配置中修改

### 组长管理提成
- 每个组员: 100元（不要求组员达标）

### 高业绩奖金
- 不累加，取最高梯度
- 达到2万: 500元
- 达到3万: 1000元
- 达到5万: 2000元

## 技术架构

- **语言**: Python 3.8+
- **UI框架**: Tkinter
- **数据处理**: pandas + openpyxl
- **配置存储**: JSON文件
- **测试框架**: pytest

### 分层架构

```
src/
├── models/        # 数据模型层
├── services/      # 业务逻辑层
├── repositories/  # 数据访问层
└── ui/            # 用户界面层
```

## 安装

### 方式一：虚拟环境（推荐）

```powershell
# 自动创建环境并安装依赖
.\scripts\setup-venv.ps1

# 激活环境
.\.venv\Scripts\Activate.ps1

# 运行程序
python main.py
```

### 方式二：全局安装

```bash
pip install -r requirements.txt
python main.py
```

## 运行

```bash
python main.py
```

## 打包

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 打包为单文件可执行程序
pyinstaller -F -w -n "绩效计算" main.py
```

输出：`dist\绩效计算.exe`

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行带覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 项目状态

已完成全部功能：
- ✅ 数据模型层（Person, Group, CommissionRule, Config）
- ✅ 业务逻辑层（提成计算逻辑）
- ✅ 数据访问层（Excel导入导出、配置持久化）
- ✅ 用户界面层（主窗口、人员管理、规则配置）
- ✅ 日志系统
- ✅ 总主管独立提成配置（v0.3.0）
- ✅ 自定义导出顺序（v0.3.0）
- ✅ 60个单元测试，全部通过

## 许可证

MIT License

---

**语言切换**: [English](README.md) | [中文](README.zh.md)