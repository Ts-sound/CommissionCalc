# CommissionCalc

一款基于 Python 开发的绩效提成自动计算工具。

## 功能特性

- Excel业绩数据导入/导出
- 可视化人员配置管理（待完善）
- 可配置的提成规则设置（待完善）
- 自动计算多种提成类型
- 详细的提成明细报表

## 提成计算规则

### 个人业绩提成
- 0-3000元: 0%
- 3000元以上: 20%（全额计算）

### 团队业绩提成（组长/总主管）
- 0-3000元: 0%
- 3000-10000元: 10%
- 10000元以上: 20%（全额计算，基于组员业绩）

### 组长管理提成
- 每个组员: 100元

### 高业绩奖金
- 达到2万: 500元
- 达到3万: 1000元（累加）
- 达到5万: 2000元（累加）

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

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 测试

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

## 项目状态

已完成核心功能：
- ✅ 数据模型层（Person, Group, CommissionRule, Config）
- ✅ 业务逻辑层（提成计算逻辑）
- ✅ 数据访问层（Excel导入导出、配置持久化）
- ✅ 48个单元测试，全部通过

待完善：
- ⏳ 用户界面完整功能
- ⏳ 人员配置管理界面
- ⏳ 提成规则配置界面

## 许可证

MIT License
