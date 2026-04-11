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
        ],
        eligible_performance_threshold=3000.0
    )
    assert config.management_bonus_per_person == 100.0
    assert len(config.high_performance_bonuses) == 3
    assert config.eligible_performance_threshold == 3000.0

def test_config_default_values():
    config = Config.default()
    assert config.management_bonus_per_person == 100.0
    assert len(config.personal_commission.tiers) == 2
    assert len(config.team_commission.tiers) == 3
    assert config.eligible_performance_threshold == 3000.0