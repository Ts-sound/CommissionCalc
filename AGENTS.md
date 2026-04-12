# CommissionCalc 项目规范

本文档帮助 AI Agent 理解项目约定，确保代码风格一致性和开发流程规范化。

## 技术栈

- **语言**: Python 3.8+
- **UI框架**: Tkinter (内置，无需额外安装)
- **数据处理**: pandas + openpyxl
- **配置存储**: JSON 文件
- **日志系统**: logging (Python 内置)
- **测试框架**: pytest + pytest-cov

## 编码规范

### 分层架构

严格遵循四层架构，禁止跨层调用：

```
src/
├── models/        # 数据模型层 - 纯数据结构，无业务逻辑
├── services/     # 业务逻辑层 - 提成计算核心逻辑
├── repositories/ # 数据访问层 - Excel/JSON 读写
└── ui/           # 用户界面层 - Tkinter 界面
```

### 模型层规范 (models/)

- 使用 `@dataclass` 定义数据类
- 类型注解必须完整
- 不包含业务逻辑，只定义数据结构
- 示例:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Person:
    id: str
    name: str
    performance: float = 0.0
    role: Role = Role.MEMBER
    group_id: Optional[str] = None
```

### 服务层规范 (services/)

- 核心业务逻辑在此实现
- 依赖注入配置和模型
- 使用 `src.utils.logger` 记录日志
- 示例:
```python
from src.utils.logger import get_logger

logger = get_logger()

class CommissionCalculator:
    def __init__(self, config: Config):
        self.config = config
        logger.debug(f"初始化提成计算器")
```

### 数据访问层规范 (repositories/)

- 负责文件 I/O 操作
- 不包含业务逻辑
- 统一异常处理

### UI层规范 (ui/)

- 使用 Tkinter 组件
- 与业务逻辑解耦，通过 services 调用
- 界面配置放在 `config/` 目录

### 代码风格

- 导入顺序: 标准库 → 第三方库 → 本地模块
- 使用 `from __future__ import annotations` 支持延迟类型注解
- 函数/方法必须有 docstring（核心逻辑）
- 类使用 PascalCase，函数/变量使用 snake_case
- 常量使用 UPPER_SNAKE_CASE
- 文件名使用 snake_case

### 日志规范

```python
from src.utils.logger import get_logger

logger = get_logger()
logger.debug("调试信息")
logger.info("重要操作")
logger.error("错误信息")
```

## 目录结构

```
CommissionCalc/
├── config/              # 配置文件目录
│   ├── config.json      # 主配置文件
│   └── commission.json  # 提成规则配置
├── docs/                # 文档目录
│   ├── design/          # 设计文档
│   ├── plans/           # 实施计划
│   ├── requirements.md  # 需求文档
│   └── terminology.md   # 术语定义
├── log/                 # 日志文件目录
├── scripts/             # 脚本目录
│   └── build.ps1        # Windows 打包脚本
├── src/                 # 源代码目录
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑
│   ├── repositories/    # 数据访问
│   ├── ui/              # 用户界面
│   └── utils/           # 工具函数
├── tests/               # 测试目录
│   ├── models/          # 模型测试
│   ├── services/        # 服务测试
│   └── repositories/    # 数据访问测试
├── main.py              # 程序入口
├── requirements.txt     # 依赖清单
├── README.md            # 项目说明
└── AGENTS.md            # 本文件
```

## 命名规范

### 文件命名

- 模块文件: `snake_case.py` (如: `calculator.py`)
- 测试文件: `test_<module>.py` (如: `test_calculator.py`)
- 数据模型: 单数名词 (如: `person.py`, `group.py`)

### 类命名

- 数据模型: 单数名词，PascalCase (如: `Person`, `Group`)
- 服务类: 功能描述 + 类型 (如: `CommissionCalculator`)
- 数据访问类: 功能 + Repo (如: `ExcelRepo`, `ConfigRepo`)

### 变量命名

- 实例变量: `snake_case` (如: `personal_commission`)
- 私有变量: `_snake_case` (如: `_calculate_team_commission`)
- 常量: `UPPER_SNAKE_CASE` (如: `DEFAULT_THRESHOLD`)

### 函数命名

- 公共方法: `snake_case` (如: `calculate_person`)
- 私有方法: `_snake_case` (如: `_validate_person`)
- 事件处理: `on_<event>` (如: `on_calculate_click`)

## Git 提交规范

### Commit 格式

```
<type>: <description>
```

### 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: add batch import feature` |
| `fix` | Bug 修复 | `fix: correct commission calculation for team leaders` |
| `refactor` | 代码重构 | `refactor: extract common validation logic` |
| `docs` | 文档更新 | `docs: update README with new features` |
| `test` | 测试相关 | `test: add unit tests for calculator` |
| `chore` | 构建/工具 | `chore: update dependencies` |
| `style` | 代码格式 | `style: format code with black` |

### 提交原则

1. 每次提交只做一件事
2. 提交信息使用英文，描述清晰
3. 功能开发使用 `feat`
4. 问题修复使用 `fix`
5. 提交前确保测试通过

## 测试规范

### 测试运行

```bash
# 运行所有测试
pytest tests/ -v

# 运行带覆盖率
pytest tests/ --cov=src --cov-report=html

# 运行特定测试文件
pytest tests/services/test_calculator.py -v
```

### 测试要求

- 新功能必须编写单元测试
- 测试覆盖率要求: ≥80%
- 测试文件与源文件目录结构对应
- 使用 `pytest.fixture` 共享测试数据

### 测试命名

- 测试类: `Test<Feature>`
- 测试方法: `test_<scenario>_<expected_result>`
- 示例:
```python
class TestCommissionCalculator:
    def test_calculate_personal_commission_below_threshold_returns_zero(self):
        ...
    
    def test_calculate_personal_commission_above_threshold_applies_rate(self):
        ...
```

## Agent 使用指南

### 新功能开发流程

```
1. @architect 设计方案 → 确认架构设计
2. @explorer 搜索相关代码 → 了解现有实现
3. @plan 制定实施计划 → 创建 Todo 列表
4. @build 实现功能 → 按计划逐步实现
5. @tester 编写测试 → 确保测试通过
6. @reviewer 审查代码 → 检查质量
```

### Bug 修复流程

```
1. @explorer 定位问题 → 找到问题代码
2. @architect 分析原因 → 确定修复方案
3. @build 修复 Bug → 实施修复
4. @tester 回归测试 → 确保无副作用
```

### 代码审查要点

```
@reviewer 审查代码，重点检查：
1. 分层是否正确（是否跨层调用）
2. 类型注解是否完整
3. 是否有日志记录
4. 测试覆盖是否充分
5. 是否遵循命名规范
```

### 常用场景示例

#### 添加新提成类型

```python
# 1. 在 models/commission.py 添加配置
# 2. 在 services/calculator.py 实现计算逻辑
# 3. 在 ui/ 添加界面配置项
# 4. 在 tests/services/test_calculator.py 添加测试
```

#### 修改提成规则

```python
# 1. 在 config/commission.json 修改配置
# 2. 在 models/commission.py 更新模型（如需）
# 3. 在 services/calculator.py 更新计算逻辑
# 4. 更新相关测试
```

#### 添加新的数据导入方式

```python
# 1. 在 repositories/ 添加新的 Repo 类
# 2. 在 services/ 添加处理逻辑
# 3. 在 ui/ 添加导入界面
# 4. 添加完整的测试覆盖
```

## 注意事项

### 禁止事项

1. ❌ UI 层直接访问 repositories
2. ❌ models 层包含业务逻辑
3. ❌ 跳过测试直接提交代码
4. ❌ 硬编码配置值（应放入配置文件）
5. ❌ 忽略类型注解

### 最佳实践

1. ✅ 保持分层架构清晰
2. ✅ 使用依赖注入
3. ✅ 编写可测试代码
4. ✅ 添加必要的日志
5. ✅ 保持代码简洁可读