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