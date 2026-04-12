# CommissionCalc 项目 Workflow 指南

本文档说明如何在 CommissionCalc 项目中使用 project-workflow skill，以及各开发场景的具体步骤。

## 概述

Workflow 是一套结构化的开发流程管理方法，确保：

1. **先思考后动手** - 设计优先，实现其次
2. **小步快跑** - 任务分解，逐步验证
3. **持续审查** - 代码审查，质量保证
4. **明确边界** - 范围清晰，风险可控

## 适用场景

### 使用 Workflow

- 复杂功能开发（涉及多模块修改）
- 架构重构
- 重大 Bug 修复
- 新模块设计

### 跳过 Workflow (Quick-Fix)

- 简单错别字修正
- 单文件小改动
- 配置参数调整
- 文档小更新

## 工作流场景

### 1. 新功能开发 (`feature_dev`)

**适用**: 添加新提成类型、新增数据导入方式、新增报表功能等

```
阶段1: brainstorming     → 设计方案，确认需求
阶段2: project-docs      → 更新设计文档
阶段3: writing-plans     → 制定实施计划
阶段4: executing-plans   → 编码实现
阶段5: requesting-code-review → 代码审查
阶段6: finishing-a-development-branch → 分支合并
```

**示例：添加奖金计算功能**

```
# 阶段1: 方案设计
@architect 设计一个年终奖金计算功能：
1. 根据累计业绩计算奖金比例
2. 支持按组别统计
3. 与现有提成计算集成

# 阶段2: 收集证据
@explorer 搜索项目中：
- 现有的提成计算逻辑 (src/services/calculator.py)
- 数据模型定义 (src/models/)
- 界面布局 (src/ui/)

# 阶段3: 明确边界
@plan 制定实施计划：
1. 在 models/commission.py 添加奖金规则配置
2. 在 services/calculator.py 实现奖金计算
3. 在 ui/ 添加奖金配置界面
4. 编写单元测试

# 阶段4: 逐步实现
@build 按计划实现，每完成一步运行测试

# 阶段5: 代码审查
@reviewer 审查代码：
- 是否遵循分层架构
- 类型注解是否完整
- 测试覆盖是否充分
```

### 2. Bug 修复 (`bug_fix`)

**适用**: 提成计算错误、数据导入异常、界面显示问题等

```
阶段1: systematic-debugging → 问题定位，原因分析
阶段2: executing-plans       → 实施修复
阶段3: verification-before-completion → 验证修复
```

**示例：修复团队提成计算错误**

```
# 阶段1: 问题定位
问题描述：组长团队提成计算时，未包含自己的业绩

@explorer 搜索所有与团队提成相关的代码
@architect 分析可能的原因：
- 计算逻辑遗漏
- 人员过滤条件错误

# 阶段2: 根因分析
查看 src/services/calculator.py 中的 _calculate_team_commission 方法

# 阶段3: 实施修复
@build 修复计算逻辑，添加日志记录

# 阶段4: 验证修复
@tester 编写回归测试，确保：
- Bug 已修复
- 其他计算不受影响
```

### 3. 代码重构 (`refactor`)

**适用**: 优化代码结构、提取公共逻辑、改进性能等

```
阶段1: brainstorming          → 重构分析，风险评估
阶段2: executing-plans        → 分步重构
阶段3: verification-before-completion → 测试验证
阶段4: requesting-code-review → 代码审查
阶段5: project-docs           → 更新文档
```

**示例：重构提成计算器**

```
# 阶段1: 分析
@architect 分析 calculator.py：
- 当前 170+ 行，职责过多
- 需要拆分个人/团队/奖金计算
- 保持 API 兼容性

# 阶段2: 计划
@plan 制定重构计划：
1. 提取个人计算函数
2. 提取团队计算函数
3. 提取奖金计算函数
4. 统一错误处理
每步保持测试通过

# 阶段3: 执行
@build 按计划重构，每步提交：
git commit -m "refactor: extract personal commission calculation"
git commit -m "refactor: extract team commission calculation"

# 阶段4: 验证
@tester 运行全部测试，对比性能

# 阶段5: 文档
@documenter 更新设计文档
```

### 4. 文档更新 (`docs_update`)

**适用**: 更新设计文档、补充 API 文档、更新需求说明等

```
阶段1: project-docs    → 分析文档需求
阶段2: executing-plans → 编写/更新文档
```

### 5. 技术调研 (`tech_research`)

**适用**: 选择新的 UI 框架、数据库迁移方案、性能优化方案等

```
阶段1: brainstorming    → 方案对比分析
阶段2: executing-plans  → 原型验证
阶段3: project-docs     → 输出调研报告
```

## 与项目结构整合

### 设计文档位置

```
docs/
├── design/           # 架构设计文档
│   ├── README.md    # 架构概述
│   └── ui-design.md # UI 设计
├── plans/           # 实施计划
│   └── YYYY-MM-DD-<name>.md
└── workflow/        # 工作流状态（可选）
    └── README.md    # 本文件
```

### Agent 角色分工

| Agent | 在 CommissionCalc 中的职责 |
|-------|---------------------------|
| `@architect` | 设计提成规则架构、数据模型设计 |
| `@explorer` | 搜索现有计算逻辑、定位配置项 |
| `@librarian` | 查找 pandas/openpyxl 最佳实践 |
| `@plan` | 分解开发任务、制定测试计划 |
| `@build` | 实现 models/services/repositories/ui |
| `@reviewer` | 检查分层架构、类型注解、测试覆盖 |
| `@tester` | 编写 pytest 测试用例 |
| `@documenter` | 更新设计文档、README |

### 任务管理

使用 TodoWrite 工具管理任务进度：

```
@plan 为"添加奖金功能"创建 Todo 列表

Todo:
- [ ] 在 models/commission.py 添加 BonusConfig
- [ ] 在 services/calculator.py 实现 calculate_bonus
- [ ] 在 ui/ 添加奖金配置界面
- [ ] 编写 test_calculator_bonus.py
```

## 开发流程示例

### 完整功能开发流程

```
# 1. 创建功能分支
git checkout -b feature/bonus-calculation

# 2. 启动工作流
# AI 自动识别场景，按阶段执行

# 3. 阶段执行
阶段1: 设计 → 确认方案
阶段2: 文档 → 更新 docs/design/
阶段3: 计划 → 创建实施计划
阶段4: 实现 → 编码 + 测试
阶段5: 审查 → 代码审查
阶段6: 完成 → 合并分支

# 4. 验证测试
pytest tests/ -v

# 5. 提交代码
git add .
git commit -m "feat: add bonus calculation feature"
```

### Bug 修复流程

```
# 1. 创建修复分支
git checkout -b fix/team-commission-bug

# 2. 定位问题
@explorer 搜索相关代码
@architect 分析根因

# 3. 修复验证
@build 修复代码
@tester 编写回归测试

# 4. 提交
git commit -m "fix: include leader's own performance in team commission"
```

## 常见问题

### Q: 什么时候跳过 Workflow？

A: 满足以下条件可使用 quick-fix：
- 修改单个文件
- 改动少于 20 行
- 不影响架构
- 不需要新增测试

### Q: 如何判断任务复杂度？

A: 参考 AGENTS.md 中的复杂度评估表：
- 低：简单修复、文档更新
- 中：单模块功能、Bug 修复
- 高：跨模块功能、架构变更

### Q: 设计文档放在哪里？

A: 
- 架构设计: `docs/design/README.md`
- UI 设计: `docs/design/ui-design.md`
- 实施计划: `docs/plans/YYYY-MM-DD-<name>.md`

### Q: 测试文件如何组织？

A: 与 src/ 目录结构对应：
```
src/services/calculator.py → tests/services/test_calculator.py
src/models/person.py → tests/models/test_person.py
```

## 最佳实践

### 1. 提交规范

```bash
# 好的提交
git commit -m "feat: add performance column customization"
git commit -m "fix: correct team commission calculation"

# 不好的提交
git commit -m "update code"
git commit -m "fix bug"
```

### 2. 分层原则

```
UI层 → 只处理用户交互
  ↓
Services层 → 只处理业务逻辑
  ↓
Repositories层 → 只处理数据访问
  ↓
Models层 → 只定义数据结构
```

### 3. 日志记录

```python
# 关键操作记录 info
logger.info(f"计算完成，共 {len(results)} 人")

# 调试信息记录 debug
logger.debug(f"个人提成={commission}")

# 错误记录 error
logger.error(f"导入失败: {e}")
```

### 4. 测试优先

```
1. 编写测试用例（描述预期行为）
2. 运行测试（应该失败）
3. 实现功能（让测试通过）
4. 重构优化（保持测试通过）
```

## 参考资料

- [项目 README](../../README.md)
- [需求文档](../requirements.md)
- [术语定义](../terminology.md)
- [架构设计](../design/README.md)
- [AGENTS.md](../../AGENTS.md) - 项目规范