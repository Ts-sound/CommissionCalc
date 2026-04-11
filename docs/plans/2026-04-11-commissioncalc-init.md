# CommissionCalc 系统实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个完整的绩效提成计算系统，支持Excel导入导出、人员配置、提成规则配置和自动计算。

**Architecture:** 采用分层架构设计，包含UI层（Tkinter）、业务逻辑层、数据访问层和模型层。核心提成计算逻辑优先测试确保准确性。

**Tech Stack:** Python 3.8+, Tkinter, pandas, openpyxl, pytest

---

## Task 1: 项目结构搭建

**Files:**
- Create: `src/__init__.py`
- Create: `src/models/__init__.py`
- Create: `src/services/__init__.py`
- Create: `src/repositories/__init__.py`
- Create: `src/ui/__init__.py`
- Create: `tests/__init__.py`
- Create: `config/__init__.py`
- Create: `requirements.txt`
- Create: `main.py`

**Step 1: 创建目录结构**

```bash
mkdir -p src/models src/services src/repositories src/ui tests config
```

**Step 2: 创建__init__.py文件**

每个__init__.py文件内容为空。

**Step 3: 创建requirements.txt**

```
pandas>=1.3.0
openpyxl>=3.0.0
pytest>=6.0.0
pytest-cov>=2.0.0
```

**Step 4: 创建main.py入口文件**

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

def main():
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
```

**Step 5: Commit**

```bash
git add src/ tests/ config/ requirements.txt main.py
git commit -m "feat: setup project structure with layered architecture"
```

---

## Task 2: 数据模型 - Role枚举

**Files:**
- Create: `src/models/role.py`
- Test: `tests/models/test_role.py`

**Step 1: Write the failing test**

```python
import pytest
from src.models.role import Role

def test_role_values():
    assert Role.GENERAL_MANAGER.value == "总主管"
    assert Role.TEAM_LEADER.value == "组长"
    assert Role.MEMBER.value == "成员"

def test_role_count():
    assert len(Role) == 3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_role.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.models.role'"

**Step 3: Write minimal implementation**

```python
from enum import Enum

class Role(Enum):
    GENERAL_MANAGER = "总主管"
    TEAM_LEADER = "组长"
    MEMBER = "成员"
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_role.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models/role.py tests/models/test_role.py
git commit -m "feat: add Role enum with tests"
```

---

## Task 3: 数据模型 - Person实体

**Files:**
- Create: `src/models/person.py`
- Test: `tests/models/test_person.py`

**Step 1: Write the failing test**

```python
import pytest
from src.models.person import Person
from src.models.role import Role

def test_person_creation():
    person = Person(
        id="test-id",
        name="张三",
        performance=5000.0,
        role=Role.TEAM_LEADER,
        group_id="group-1"
    )
    assert person.id == "test-id"
    assert person.name == "张三"
    assert person.performance == 5000.0
    assert person.role == Role.TEAM_LEADER
    assert person.group_id == "group-1"

def test_person_optional_group():
    person = Person(
        id="gm-id",
        name="总主管",
        performance=10000.0,
        role=Role.GENERAL_MANAGER
    )
    assert person.group_id is None

def test_person_default_performance():
    person = Person(
        id="member-id",
        name="成员",
        role=Role.MEMBER
    )
    assert person.performance == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_person.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from typing import Optional
from src.models.role import Role

@dataclass
class Person:
    id: str
    name: str
    performance: float = 0.0
    role: Role = Role.MEMBER
    group_id: Optional[str] = None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_person.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models/person.py tests/models/test_person.py
git commit -m "feat: add Person dataclass with tests"
```

---

## Task 4: 数据模型 - Group实体

**Files:**
- Create: `src/models/group.py`
- Test: `tests/models/test_group.py`

**Step 1: Write the failing test**

```python
import pytest
from src.models.group import Group

def test_group_creation():
    group = Group(
        id="group-1",
        name="A组",
        leader_id="leader-1",
        members=["member-1", "member-2"]
    )
    assert group.id == "group-1"
    assert group.name == "A组"
    assert group.leader_id == "leader-1"
    assert group.members == ["member-1", "member-2"]

def test_group_default_members():
    group = Group(
        id="group-2",
        name="B组",
        leader_id="leader-2"
    )
    assert group.members == []

def test_add_member():
    group = Group(id="g1", name="Group", leader_id="l1", members=[])
    group.add_member("m1")
    assert "m1" in group.members

def test_remove_member():
    group = Group(id="g1", name="Group", leader_id="l1", members=["m1", "m2"])
    group.remove_member("m1")
    assert "m1" not in group.members
    assert "m2" in group.members
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_group.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Group:
    id: str
    name: str
    leader_id: str
    members: List[str] = field(default_factory=list)
    
    def add_member(self, member_id: str):
        if member_id not in self.members:
            self.members.append(member_id)
    
    def remove_member(self, member_id: str):
        if member_id in self.members:
            self.members.remove(member_id)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_group.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models/group.py tests/models/test_group.py
git commit -m "feat: add Group dataclass with tests"
```

---

## Task 5: 数据模型 - CommissionRule和Tier

**Files:**
- Create: `src/models/commission.py`
- Test: `tests/models/test_commission.py`

**Step 1: Write the failing test**

```python
import pytest
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

def test_tier_creation():
    tier = Tier(min_amount=0, max_amount=3000, rate=0.0)
    assert tier.min_amount == 0
    assert tier.max_amount == 3000
    assert tier.rate == 0.0

def test_tier_unlimited_max():
    tier = Tier(min_amount=3000, max_amount=None, rate=0.2)
    assert tier.max_amount is None

def test_rule_type_values():
    assert RuleType.PERSONAL.value == "个人业绩提成"
    assert RuleType.TEAM.value == "团队业绩提成"
    assert RuleType.HIGH_BONUS.value == "高业绩奖金"

def test_commission_rule_creation():
    rule = CommissionRule(
        rule_type=RuleType.PERSONAL,
        tiers=[
            Tier(min_amount=0, max_amount=3000, rate=0.0),
            Tier(min_amount=3000, max_amount=None, rate=0.2)
        ]
    )
    assert rule.rule_type == RuleType.PERSONAL
    assert len(rule.tiers) == 2

def test_bonus_creation():
    bonus = Bonus(threshold=20000, amount=500)
    assert bonus.threshold == 20000
    assert bonus.amount == 500
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_commission.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class RuleType(Enum):
    PERSONAL = "个人业绩提成"
    TEAM = "团队业绩提成"
    HIGH_BONUS = "高业绩奖金"

@dataclass
class Tier:
    min_amount: float
    max_amount: Optional[float]
    rate: float

@dataclass
class Bonus:
    threshold: float
    amount: float

@dataclass
class CommissionRule:
    rule_type: RuleType
    tiers: List[Tier]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_commission.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models/commission.py tests/models/test_commission.py
git commit -m "feat: add CommissionRule, Tier, Bonus models with tests"
```

---

## Task 6: 数据模型 - Config配置

**Files:**
- Create: `src/models/config.py`
- Test: `tests/models/test_config.py`

**Step 1: Write the failing test**

```python
import pytest
from src.models.config import Config
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

def test_config_creation():
    config = Config(
        personal_commission=CommissionRule(
            rule_type=RuleType.PERSONAL,
            tiers=[
                Tier(min_amount=0, max_amount=3000, rate=0.0),
                Tier(min_amount=3000, max_amount=None, rate=0.2)
            ]
        ),
        team_commission=CommissionRule(
            rule_type=RuleType.TEAM,
            tiers=[
                Tier(min_amount=0, max_amount=3000, rate=0.0),
                Tier(min_amount=3000, max_amount=10000, rate=0.1),
                Tier(min_amount=10000, max_amount=None, rate=0.2)
            ]
        ),
        management_bonus_per_person=100.0,
        high_performance_bonuses=[
            Bonus(threshold=20000, amount=500),
            Bonus(threshold=30000, amount=1000),
            Bonus(threshold=50000, amount=2000)
        ]
    )
    assert config.management_bonus_per_person == 100.0
    assert len(config.high_performance_bonuses) == 3

def test_config_default_values():
    config = Config.default()
    assert config.management_bonus_per_person == 100.0
    assert len(config.personal_commission.tiers) == 2
    assert len(config.team_commission.tiers) == 3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_config.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from typing import List
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

@dataclass
class Config:
    personal_commission: CommissionRule
    team_commission: CommissionRule
    management_bonus_per_person: float
    high_performance_bonuses: List[Bonus]
    
    @classmethod
    def default(cls) -> Config:
        return cls(
            personal_commission=CommissionRule(
                rule_type=RuleType.PERSONAL,
                tiers=[
                    Tier(min_amount=0, max_amount=3000, rate=0.0),
                    Tier(min_amount=3000, max_amount=None, rate=0.2)
                ]
            ),
            team_commission=CommissionRule(
                rule_type=RuleType.TEAM,
                tiers=[
                    Tier(min_amount=0, max_amount=3000, rate=0.0),
                    Tier(min_amount=3000, max_amount=10000, rate=0.1),
                    Tier(min_amount=10000, max_amount=None, rate=0.2)
                ]
            ),
            management_bonus_per_person=100.0,
            high_performance_bonuses=[
                Bonus(threshold=20000, amount=500),
                Bonus(threshold=30000, amount=1000),
                Bonus(threshold=50000, amount=2000)
            ]
        )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/models/config.py tests/models/test_config.py
git commit -m "feat: add Config model with default values and tests"
```

---

## Task 7: 业务逻辑 - 个人提成计算

**Files:**
- Create: `src/services/calculator.py`
- Test: `tests/services/test_calculator_personal.py`

**Step 1: Write the failing test**

```python
import pytest
from src.services.calculator import calculate_personal_commission
from src.models.commission import CommissionRule, Tier, RuleType

@pytest.fixture
def personal_rule():
    return CommissionRule(
        rule_type=RuleType.PERSONAL,
        tiers=[
            Tier(min_amount=0, max_amount=3000, rate=0.0),
            Tier(min_amount=3000, max_amount=None, rate=0.2)
        ]
    )

def test_personal_commission_below_threshold(personal_rule):
    assert calculate_personal_commission(2500, personal_rule) == 0.0

def test_personal_commission_at_threshold(personal_rule):
    assert calculate_personal_commission(3000, personal_rule) == 600.0

def test_personal_commission_above_threshold(personal_rule):
    assert calculate_personal_commission(5000, personal_rule) == 1000.0

def test_personal_commission_high_amount(personal_rule):
    assert calculate_personal_commission(15000, personal_rule) == 3000.0

def test_personal_commission_zero(personal_rule):
    assert calculate_personal_commission(0, personal_rule) == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/services/test_calculator_personal.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
from src.models.commission import CommissionRule

def calculate_personal_commission(performance: float, rule: CommissionRule) -> float:
    if performance <= 0:
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= performance:
            if tier.max_amount is None or performance < tier.max_amount:
                return performance * tier.rate
    
    return 0.0
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/services/test_calculator_personal.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/services/calculator.py tests/services/test_calculator_personal.py
git commit -m "feat: add personal commission calculation with tests"
```

---

## Task 8: 业务逻辑 - 团队提成计算

**Files:**
- Modify: `src/services/calculator.py`
- Test: `tests/services/test_calculator_team.py`

**Step 1: Write the failing test**

```python
import pytest
from src.services.calculator import calculate_team_commission
from src.models.commission import CommissionRule, Tier, RuleType

@pytest.fixture
def team_rule():
    return CommissionRule(
        rule_type=RuleType.TEAM,
        tiers=[
            Tier(min_amount=0, max_amount=3000, rate=0.0),
            Tier(min_amount=3000, max_amount=10000, rate=0.1),
            Tier(min_amount=10000, max_amount=None, rate=0.2)
        ]
    )

def test_team_commission_below_threshold(team_rule):
    assert calculate_team_commission(2500, team_rule) == 0.0

def test_team_commission_tier1(team_rule):
    assert calculate_team_commission(5000, team_rule) == 500.0

def test_team_commission_at_10000(team_rule):
    assert calculate_team_commission(10000, team_rule) == 2000.0

def test_team_commission_above_10000(team_rule):
    assert calculate_team_commission(15000, team_rule) == 3000.0

def test_team_commission_zero(team_rule):
    assert calculate_team_commission(0, team_rule) == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/services/test_calculator_team.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Add to `src/services/calculator.py`:

```python
def calculate_team_commission(team_performance: float, rule: CommissionRule) -> float:
    if team_performance <= 0:
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= team_performance:
            if tier.max_amount is None or team_performance < tier.max_amount:
                return team_performance * tier.rate
    
    return 0.0
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/services/test_calculator_team.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/services/calculator.py tests/services/test_calculator_team.py
git commit -m "feat: add team commission calculation with tests"
```

---

## Task 9: 业务逻辑 - 管理提成计算

**Files:**
- Modify: `src/services/calculator.py`
- Test: `tests/services/test_calculator_management.py`

**Step 1: Write the failing test**

```python
import pytest
from src.services.calculator import calculate_management_bonus

def test_management_bonus_1_member():
    assert calculate_management_bonus(1, 100.0) == 100.0

def test_management_bonus_3_members():
    assert calculate_management_bonus(3, 100.0) == 300.0

def test_management_bonus_10_members():
    assert calculate_management_bonus(10, 100.0) == 1000.0

def test_management_bonus_zero_members():
    assert calculate_management_bonus(0, 100.0) == 0.0

def test_management_bonus_custom_rate():
    assert calculate_management_bonus(5, 150.0) == 750.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/services/test_calculator_management.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Add to `src/services/calculator.py`:

```python
def calculate_management_bonus(member_count: int, bonus_per_person: float) -> float:
    return member_count * bonus_per_person
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/services/test_calculator_management.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/services/calculator.py tests/services/test_calculator_management.py
git commit -m "feat: add management bonus calculation with tests"
```

---

## Task 10: 业务逻辑 - 高业绩奖金计算

**Files:**
- Modify: `src/services/calculator.py`
- Test: `tests/services/test_calculator_bonus.py`

**Step 1: Write the failing test**

```python
import pytest
from src.services.calculator import calculate_high_performance_bonus
from src.models.commission import Bonus

@pytest.fixture
def bonuses():
    return [
        Bonus(threshold=20000, amount=500),
        Bonus(threshold=30000, amount=1000),
        Bonus(threshold=50000, amount=2000)
    ]

def test_bonus_below_20000(bonuses):
    assert calculate_high_performance_bonus(15000, bonuses) == 0.0

def test_bonus_at_20000(bonuses):
    assert calculate_high_performance_bonus(20000, bonuses) == 500.0

def test_bonus_25000(bonuses):
    assert calculate_high_performance_bonus(25000, bonuses) == 500.0

def test_bonus_at_30000(bonuses):
    assert calculate_high_performance_bonus(30000, bonuses) == 1500.0

def test_bonus_35000(bonuses):
    assert calculate_high_performance_bonus(35000, bonuses) == 1500.0

def test_bonus_at_50000(bonuses):
    assert calculate_high_performance_bonus(50000, bonuses) == 3500.0

def test_bonus_55000(bonuses):
    assert calculate_high_performance_bonus(55000, bonuses) == 3500.0

def test_bonus_empty_list():
    assert calculate_high_performance_bonus(30000, []) == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/services/test_calculator_bonus.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Add to `src/services/calculator.py`:

```python
from typing import List
from src.models.commission import Bonus

def calculate_high_performance_bonus(performance: float, bonuses: List[Bonus]) -> float:
    total_bonus = 0.0
    for bonus in bonuses:
        if performance >= bonus.threshold:
            total_bonus += bonus.amount
    return total_bonus
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/services/test_calculator_bonus.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/services/calculator.py tests/services/test_calculator_bonus.py
git commit -m "feat: add high performance bonus calculation with tests"
```

---

## Task 11: 业务逻辑 - 完整提成计算器

**Files:**
- Modify: `src/services/calculator.py`
- Test: `tests/services/test_calculator_complete.py`

**Step 1: Write the failing test**

```python
import pytest
from src.services.calculator import CommissionCalculator
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.models.config import Config

@pytest.fixture
def calculator():
    return CommissionCalculator(Config.default())

@pytest.fixture
def sample_people():
    return {
        "gm": Person(id="gm", name="总主管", performance=5000, role=Role.GENERAL_MANAGER),
        "leader1": Person(id="leader1", name="组长A", performance=5000, role=Role.TEAM_LEADER, group_id="group1"),
        "member1": Person(id="member1", name="成员A1", performance=5000, role=Role.MEMBER, group_id="group1"),
        "member2": Person(id="member2", name="成员A2", performance=3000, role=Role.MEMBER, group_id="group1"),
    }

@pytest.fixture
def sample_groups():
    return {
        "group1": Group(id="group1", name="A组", leader_id="leader1", members=["member1", "member2"])
    }

def test_calculate_person_commission(calculator, sample_people):
    result = calculator.calculate_person(sample_people["member1"])
    assert result.personal_commission == 1000.0
    assert result.management_bonus == 0.0
    assert result.total == result.personal_commission

def test_calculate_leader_commission(calculator, sample_people, sample_groups):
    calculator.set_groups(sample_groups)
    calculator.set_people(sample_people)
    
    result = calculator.calculate_person(sample_people["leader1"])
    assert result.personal_commission == 1000.0
    assert result.team_commission == 1600.0  # (5000+3000) * 0.2
    assert result.management_bonus == 200.0  # 2 members * 100
    assert result.total == 2800.0

def test_calculate_general_manager_commission(calculator, sample_people, sample_groups):
    calculator.set_groups(sample_groups)
    calculator.set_people(sample_people)
    
    result = calculator.calculate_person(sample_people["gm"])
    assert result.personal_commission == 1000.0
    assert result.team_commission == 2600.0  # (5000+5000+3000+5000) * 0.2
    assert result.management_bonus == 0.0
    assert result.total == 3600.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/services/test_calculator_complete.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Add to `src/services/calculator.py`:

```python
from dataclasses import dataclass
from typing import Dict
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.models.config import Config

@dataclass
class CommissionResult:
    person_id: str
    personal_commission: float = 0.0
    team_commission: float = 0.0
    management_bonus: float = 0.0
    high_performance_bonus: float = 0.0
    total: float = 0.0

class CommissionCalculator:
    def __init__(self, config: Config):
        self.config = config
        self.people: Dict[str, Person] = {}
        self.groups: Dict[str, Group] = {}
    
    def set_people(self, people: Dict[str, Person]):
        self.people = people
    
    def set_groups(self, groups: Dict[str, Group]):
        self.groups = groups
    
    def calculate_person(self, person: Person) -> CommissionResult:
        result = CommissionResult(person_id=person.id)
        
        result.personal_commission = calculate_personal_commission(
            person.performance, self.config.personal_commission
        )
        
        if person.role in [Role.TEAM_LEADER, Role.GENERAL_MANAGER]:
            result.team_commission = self._calculate_team_commission(person)
        
        if person.role == Role.TEAM_LEADER:
            result.management_bonus = self._calculate_management_bonus(person)
        
        result.high_performance_bonus = calculate_high_performance_bonus(
            person.performance, self.config.high_performance_bonuses
        )
        
        result.total = (
            result.personal_commission +
            result.team_commission +
            result.management_bonus +
            result.high_performance_bonus
        )
        
        return result
    
    def _calculate_team_commission(self, person: Person) -> float:
        if person.role == Role.GENERAL_MANAGER:
            team_performance = sum(p.performance for p in self.people.values())
        else:
            group = self.groups.get(person.group_id)
            if group:
                team_performance = sum(
                    self.people[mid].performance 
                    for mid in group.members 
                    if mid in self.people
                )
            else:
                team_performance = 0.0
        
        return calculate_team_commission(team_performance, self.config.team_commission)
    
    def _calculate_management_bonus(self, person: Person) -> float:
        group = self.groups.get(person.group_id)
        if group:
            return calculate_management_bonus(
                len(group.members), self.config.management_bonus_per_person
            )
        return 0.0
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/services/test_calculator_complete.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/services/calculator.py tests/services/test_calculator_complete.py
git commit -m "feat: add CommissionCalculator class with complete calculation logic"
```

---

## Task 12: 数据访问 - 配置仓库

**Files:**
- Create: `src/repositories/config_repo.py`
- Test: `tests/repositories/test_config_repo.py`

**Step 1: Write the failing test**

```python
import pytest
import os
import json
import tempfile
from src.repositories.config_repo import ConfigRepository
from src.models.config import Config

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def config_repo(temp_dir):
    return ConfigRepository(temp_dir)

def test_save_config(config_repo):
    config = Config.default()
    config_repo.save(config)
    
    config_file = os.path.join(config_repo.config_dir, "settings.json")
    assert os.path.exists(config_file)
    
    with open(config_file) as f:
        data = json.load(f)
    assert data["management_bonus_per_person"] == 100.0

def test_load_config(config_repo):
    config = Config.default()
    config_repo.save(config)
    
    loaded_config = config_repo.load()
    assert loaded_config.management_bonus_per_person == 100.0
    assert len(loaded_config.personal_commission.tiers) == 2

def test_load_default_if_not_exists(config_repo):
    loaded_config = config_repo.load()
    assert loaded_config.management_bonus_per_person == 100.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/repositories/test_config_repo.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
import os
import json
from src.models.config import Config
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

class ConfigRepository:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
    
    def save(self, config: Config):
        config_file = os.path.join(self.config_dir, "settings.json")
        
        data = {
            "personal_commission": {
                "rule_type": config.personal_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.personal_commission.tiers
                ]
            },
            "team_commission": {
                "rule_type": config.team_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.team_commission.tiers
                ]
            },
            "management_bonus_per_person": config.management_bonus_per_person,
            "high_performance_bonuses": [
                {"threshold": b.threshold, "amount": b.amount}
                for b in config.high_performance_bonuses
            ]
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> Config:
        config_file = os.path.join(self.config_dir, "settings.json")
        
        if not os.path.exists(config_file):
            return Config.default()
        
        with open(config_file, encoding='utf-8') as f:
            data = json.load(f)
        
        return Config(
            personal_commission=CommissionRule(
                rule_type=RuleType(data["personal_commission"]["rule_type"]),
                tiers=[
                    Tier(**t) for t in data["personal_commission"]["tiers"]
                ]
            ),
            team_commission=CommissionRule(
                rule_type=RuleType(data["team_commission"]["rule_type"]),
                tiers=[
                    Tier(**t) for t in data["team_commission"]["tiers"]
                ]
            ),
            management_bonus_per_person=data["management_bonus_per_person"],
            high_performance_bonuses=[
                Bonus(**b) for b in data["high_performance_bonuses"]
            ]
        )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/repositories/test_config_repo.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/repositories/config_repo.py tests/repositories/test_config_repo.py
git commit -m "feat: add ConfigRepository for JSON persistence with tests"
```

---

## Task 13: 数据访问 - Excel仓库

**Files:**
- Create: `src/repositories/excel_repo.py`
- Test: `tests/repositories/test_excel_repo.py`

**Step 1: Write the failing test**

```python
import pytest
import pandas as pd
import tempfile
import os
from src.repositories.excel_repo import ExcelRepository

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def excel_repo(temp_dir):
    return ExcelRepository()

@pytest.fixture
def sample_excel_file(temp_dir):
    df = pd.DataFrame({
        "姓名": ["张三", "李四", "王五"],
        "业绩": [5000, 3000, 15000]
    })
    file_path = os.path.join(temp_dir, "test.xlsx")
    df.to_excel(file_path, index=False)
    return file_path

def test_import_performance_data(excel_repo, sample_excel_file):
    data = excel_repo.import_performance_data(sample_excel_file)
    
    assert len(data) == 3
    assert data["张三"] == 5000.0
    assert data["李四"] == 3000.0
    assert data["王五"] == 15000.0

def test_import_missing_column(excel_repo, temp_dir):
    df = pd.DataFrame({"姓名": ["张三"]})
    file_path = os.path.join(temp_dir, "invalid.xlsx")
    df.to_excel(file_path, index=False)
    
    with pytest.raises(ValueError, match="缺少'业绩'列"):
        excel_repo.import_performance_data(file_path)

def test_export_results(excel_repo, temp_dir):
    results = [
        {
            "姓名": "张三",
            "业绩": 5000,
            "身份": "组长",
            "组别": "A组",
            "个人提成": 1000,
            "团队提成": 800,
            "管理提成": 200,
            "高业绩奖金": 500,
            "总提成": 2500
        }
    ]
    
    export_path = os.path.join(temp_dir, "result.xlsx")
    excel_repo.export_results(results, export_path)
    
    assert os.path.exists(export_path)
    
    df = pd.read_excel(export_path)
    assert len(df) == 1
    assert df.iloc[0]["姓名"] == "张三"
    assert df.iloc[0]["总提成"] == 2500
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/repositories/test_excel_repo.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
import pandas as pd
from typing import Dict, List

class ExcelRepository:
    def import_performance_data(self, file_path: str) -> Dict[str, float]:
        df = pd.read_excel(file_path)
        
        if "姓名" not in df.columns:
            raise ValueError("缺少'姓名'列")
        
        if "业绩" not in df.columns:
            raise ValueError("缺少'业绩'列")
        
        data = {}
        for _, row in df.iterrows():
            name = str(row["姓名"])
            performance = float(row["业绩"])
            data[name] = performance
        
        return data
    
    def export_results(self, results: List[Dict], file_path: str):
        df = pd.DataFrame(results)
        df.to_excel(file_path, index=False)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/repositories/test_excel_excel_repo.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/repositories/excel_repo.py tests/repositories/test_excel_repo.py
git commit -m "feat: add ExcelRepository for import/export with tests"
```

---

## Task 14: 用户界面 - 主窗口基础

**Files:**
- Create: `src/ui/main_window.py`

**Step 1: Create main window skeleton**

```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("绩效提成计算系统")
        self.root.geometry("800x600")
        
        self._create_menu()
        self._create_main_frame()
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="导入业绩", command=self.import_performance)
        file_menu.add_command(label="导出结果", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        menubar.add_cascade(label="文件", menu=file_menu)
        
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="人员管理", command=self.open_person_config)
        config_menu.add_command(label="提成规则", command=self.open_commission_config)
        
        menubar.add_cascade(label="配置", menu=config_menu)
        
        self.root.config(menu=menubar)
    
    def _create_main_frame(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        file_frame = ttk.LabelFrame(main_frame, text="业绩文件", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=0)
        ttk.Button(file_frame, text="选择文件", command=self.select_file).grid(row=0, column=1)
        
        preview_frame = ttk.LabelFrame(main_frame, text="业绩数据预览", padding="5")
        preview_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.preview_tree = ttk.Treeview(preview_frame, columns=("姓名", "业绩", "身份", "组别"), show="headings")
        self.preview_tree.heading("姓名", text="姓名")
        self.preview_tree.heading("业绩", text="业绩")
        self.preview_tree.heading("身份", text="身份")
        self.preview_tree.heading("组别", text="组别")
        self.preview_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(main_frame, text="计算提成", command=self.calculate_commission).grid(row=2, column=0, columnspan=2)
        
        result_frame = ttk.LabelFrame(main_frame, text="结果汇总", padding="5")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_tree = ttk.Treeview(
            result_frame, 
            columns=("姓名", "个人提成", "团队提成", "管理提成", "奖金", "总计"),
            show="headings"
        )
        for col in self.result_tree["columns"]:
            self.result_tree.heading(col, text=col)
        self.result_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def select_file(self):
        pass
    
    def import_performance(self):
        pass
    
    def export_results(self):
        pass
    
    def open_person_config(self):
        pass
    
    def open_commission_config(self):
        pass
    
    def calculate_commission(self):
        pass
    
    def run(self):
        self.root.mainloop()
```

**Step 2: Verify window can be created**

Manual test: Run `python main.py` and verify window appears.

**Step 3: Commit**

```bash
git add src/ui/main_window.py
git commit -m "feat: add MainWindow skeleton with menu and basic layout"
```

---

## Task 15: 用户界面 - 文件选择功能

**Files:**
- Modify: `src/ui/main_window.py`

**Step 1: Implement file selection**

Add imports:
```python
from src.repositories.excel_repo import ExcelRepository
```

Add attributes in __init__:
```python
self.excel_repo = ExcelRepository()
self.performance_data = {}
```

Implement select_file:
```python
def select_file(self):
    file_path = filedialog.askopenfilename(
        title="选择业绩Excel文件",
        filetypes=[("Excel文件", "*.xlsx *.xls")]
    )
    if file_path:
        self.file_path_var.set(file_path)
        self.load_performance_data(file_path)
```

Implement load_performance_data:
```python
def load_performance_data(self, file_path: str):
    try:
        self.performance_data = self.excel_repo.import_performance_data(file_path)
        self.update_preview()
    except ValueError as e:
        messagebox.showerror("导入失败", str(e))
```

Implement update_preview:
```python
def update_preview(self):
    for item in self.preview_tree.get_children():
        self.preview_tree.delete(item)
    
    for name, performance in self.performance_data.items():
        self.preview_tree.insert("", tk.END, values=(name, performance, "", ""))
```

**Step 2: Manual test**

Run `python main.py`, click "选择文件", select a valid Excel file with "姓名" and "业绩" columns. Verify data appears in preview.

**Step 3: Commit**

```bash
git add src/ui/main_window.py
git commit -m "feat: add file selection and performance data loading"
```

---

## Task 16: 用户界面 - 人员配置窗口

**Files:**
- Create: `src/ui/config_panel.py`

**Step 1: Create person config dialog**

```python
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role

class PersonConfigDialog:
    def __init__(self, parent, people: Dict[str, Person], groups: Dict[str, Group]):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("人员配置")
        self.dialog.geometry("600x400")
        
        self.people = people
        self.groups = groups
        
        self._create_widgets()
    
    def _create_widgets(self):
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        person_tab = ttk.Frame(notebook)
        notebook.add(person_tab, text="人员管理")
        self._create_person_tab(person_tab)
        
        group_tab = ttk.Frame(notebook)
        notebook.add(group_tab, text="组别管理")
        self._create_group_tab(group_tab)
    
    def _create_person_tab(self, parent):
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("姓名", "身份", "组别")
        self.person_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.person_tree.heading(col, text=col)
            self.person_tree.column(col, width=150)
        
        self.person_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.person_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.person_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_person_list()
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="添加", command=self.add_person).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="编辑", command=self.edit_person).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="删除", command=self.delete_person).pack(side=tk.LEFT)
    
    def _create_group_tab(self, parent):
        pass
    
    def refresh_person_list(self):
        for item in self.person_tree.get_children():
            self.person_tree.delete(item)
        
        for person in self.people.values():
            group_name = self.groups.get(person.group_id, "").name if person.group_id else ""
            self.person_tree.insert("", tk.END, values=(
                person.name, person.role.value, group_name
            ))
    
    def add_person(self):
        pass
    
    def edit_person(self):
        pass
    
    def delete_person(self):
        pass
```

**Step 2: Commit**

```bash
git add src/ui/config_panel.py
git commit -m "feat: add PersonConfigDialog skeleton"
```

---

## Task 17: 用户界面 - 集成配置窗口

**Files:**
- Modify: `src/ui/main_window.py`
- Modify: `src/ui/config_panel.py`

**Step 1: Add people and groups management to MainWindow**

Add imports:
```python
from src.ui.config_panel import PersonConfigDialog
from src.models.person import Person
from src.models.group import Group
```

Add attributes in __init__:
```python
self.people: Dict[str, Person] = {}
self.groups: Dict[str, Group] = {}
```

Implement open_person_config:
```python
def open_person_config(self):
    dialog = PersonConfigDialog(self.root, self.people, self.groups)
    self.dialog.wait_window(dialog.dialog)
```

**Step 2: Update preview to show person info**

Modify update_preview in main_window.py:
```python
def update_preview(self):
    for item in self.preview_tree.get_children():
        self.preview_tree.delete(item)
    
    for name, performance in self.performance_data.items():
        person = next((p for p in self.people.values() if p.name == name), None)
        if person:
            group_name = self.groups.get(person.group_id, "").name if person.group_id else ""
            self.preview_tree.insert("", tk.END, values=(
                name, performance, person.role.value, group_name
            ))
        else:
            self.preview_tree.insert("", tk.END, values=(name, performance, "", ""))
```

**Step 3: Commit**

```bash
git add src/ui/main_window.py src/ui/config_panel.py
git commit -m "feat: integrate person config dialog with main window"
```

---

## Task 18: 完整测试套件运行

**Files:**
- All test files

**Step 1: Run all tests**

Run: `pytest tests/ -v --cov=src`

Expected: All tests PASS, coverage > 80%

**Step 2: Fix any failures**

If any tests fail, debug and fix the issues.

**Step 3: Generate coverage report**

Run: `pytest tests/ --cov=src --cov-report=html`

**Step 4: Commit final test verification**

```bash
git commit --allow-empty -m "test: verify all tests pass with coverage"
```

---

## Task 19: 创建README使用说明

**Files:**
- Modify: `README.md`

**Step 1: Update README**

```markdown
# CommissionCalc

一款基于 Python 开发的绩效提成自动计算工具。

## 功能特性

- Excel业绩数据导入/导出
- 可视化人员配置管理
- 可配置的提成规则设置
- 自动计算多种提成类型
- 详细的提成明细报表

## 安装

### 依赖安装

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 使用指南

### 1. 导入业绩数据

点击"文件 → 导入业绩"或主界面"选择文件"按钮，选择包含"姓名"和"业绩"列的Excel文件。

### 2. 配置人员信息

点击"配置 → 人员管理"，为导入的人员分配身份（总主管/组长/成员）和组别。

### 3. 配置提成规则

点击"配置 → 提成规则"，设置各类提成的阶梯比例和奖金规则。

### 4. 计算提成

点击"计算提成"按钮，系统将自动计算所有人员的提成。

### 5. 导出结果

点击"文件 → 导出结果"，将计算结果导出为Excel文件。

## 提成计算规则

### 个人业绩提成
- 0-3000元: 0%
- 3000元以上: 20%

### 团队业绩提成（组长/总主管）
- 0-3000元: 0%
- 3000-10000元: 10%
- 10000元以上: 20%

### 组长管理提成
- 每个组员: 100元

### 高业绩奖金
- 达到2万: 500元
- 达到3万: 1000元
- 达到5万: 2000元

## 技术架构

- **UI层**: Tkinter界面
- **业务逻辑层**: 提成计算服务
- **数据访问层**: Excel/配置仓库
- **模型层**: Person, Group, CommissionRule等

## 开发

### 运行测试

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

### 目录结构

```
CommissionCalc/
├── src/           # 源代码
│   ├── models/    # 数据模型
│   ├── services/  # 业务逻辑
│   ├── repositories/ # 数据访问
│   └── ui/        # 用户界面
├── tests/         # 单元测试
├── config/        # 配置文件
├── docs/          # 文档
└── main.py        # 程序入口
```

## 许可证

MIT License
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with usage guide and features"
```

---

## Task 20: 最终验证和打包

**Files:**
- All project files

**Step 1: Final test run**

Run: `pytest tests/ -v`

Expected: All tests PASS

**Step 2: Manual integration test**

1. Run `python main.py`
2. Import a sample Excel file
3. Configure persons
4. Calculate commissions
5. Export results
6. Verify Excel output is correct

**Step 3: Check file structure**

Run: `tree -L 3 -I '__pycache__|*.pyc|.git'`

Verify structure matches design document.

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete CommissionCalc system implementation"
```

---

## 执行顺序总结

1. **项目结构** (Task 1)
2. **数据模型** (Tasks 2-6): Role, Person, Group, CommissionRule, Config
3. **业务逻辑** (Tasks 7-11): 各类提成计算
4. **数据访问** (Tasks 12-13): Config和Excel仓库
5. **用户界面** (Tasks 14-17): 主窗口和配置面板
6. **测试验证** (Task 18)
7. **文档** (Task 19)
8. **最终验证** (Task 20)

每一步都遵循TDD原则：先写测试，再实现，确保质量。