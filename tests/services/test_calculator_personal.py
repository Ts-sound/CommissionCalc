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
    commission, rate = calculate_personal_commission(2500, personal_rule)
    assert commission == 0.0
    assert rate == 0.0

def test_personal_commission_at_threshold(personal_rule):
    commission, rate = calculate_personal_commission(3000, personal_rule)
    assert commission == 600.0
    assert rate == 0.2

def test_personal_commission_above_threshold(personal_rule):
    commission, rate = calculate_personal_commission(5000, personal_rule)
    assert commission == 1000.0
    assert rate == 0.2

def test_personal_commission_high_amount(personal_rule):
    commission, rate = calculate_personal_commission(15000, personal_rule)
    assert commission == 3000.0
    assert rate == 0.2

def test_personal_commission_zero(personal_rule):
    commission, rate = calculate_personal_commission(0, personal_rule)
    assert commission == 0.0
    assert rate == 0.0