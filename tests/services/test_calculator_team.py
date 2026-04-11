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