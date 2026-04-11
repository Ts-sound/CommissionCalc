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