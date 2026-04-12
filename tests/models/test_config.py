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
                Tier(min_amount=0, max_amount=10000, rate=0.0),
                Tier(min_amount=10000, max_amount=50000, rate=0.1),
                Tier(min_amount=50000, max_amount=None, rate=0.2)
            ]
        ),
        gm_commission=CommissionRule(
            rule_type=RuleType.GM,
            tiers=[
                Tier(min_amount=0, max_amount=50000, rate=0.0),
                Tier(min_amount=50000, max_amount=None, rate=0.1)
            ]
        ),
        temp_leader_commission=CommissionRule(
            rule_type=RuleType.TEAM,
            tiers=[
                Tier(min_amount=0, max_amount=10000, rate=0.0),
                Tier(min_amount=10000, max_amount=50000, rate=0.1),
                Tier(min_amount=50000, max_amount=None, rate=0.2)
            ]
        ),
        branch_manager_commission=CommissionRule(
            rule_type=RuleType.GM,
            tiers=[
                Tier(min_amount=0, max_amount=50000, rate=0.0),
                Tier(min_amount=50000, max_amount=None, rate=0.1)
            ]
        ),
        management_bonus_per_person=100.0,
        high_performance_bonuses=[
            Bonus(threshold=20000, amount=500),
            Bonus(threshold=30000, amount=1000),
            Bonus(threshold=50000, amount=2000)
        ],
        eligible_performance_threshold=3000.0,
        gm_eligible_threshold=50000.0
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

def test_config_gm_fields():
    config = Config.default()
    assert config.gm_eligible_threshold == 50000.0
    assert len(config.gm_commission.tiers) == 2
    assert config.gm_commission.tiers[0].rate == 0.0
    assert config.gm_commission.tiers[1].rate == 0.1

def test_config_gm_threshold_default():
    config = Config.default()
    assert config.gm_eligible_threshold == 50000.0

def test_config_temp_leader_commission_default():
    config = Config.default()
    assert hasattr(config, 'temp_leader_commission')
    assert len(config.temp_leader_commission.tiers) == 3
    assert config.temp_leader_commission.tiers[0].min_amount == 0
    assert config.temp_leader_commission.tiers[0].max_amount == 10000
    assert config.temp_leader_commission.tiers[0].rate == 0.0
    assert config.temp_leader_commission.tiers[1].min_amount == 10000
    assert config.temp_leader_commission.tiers[1].max_amount == 50000
    assert config.temp_leader_commission.tiers[1].rate == 0.1
    assert config.temp_leader_commission.tiers[2].min_amount == 50000
    assert config.temp_leader_commission.tiers[2].max_amount is None
    assert config.temp_leader_commission.tiers[2].rate == 0.2

def test_config_temp_leader_eligible_threshold_default():
    config = Config.default()
    assert config.temp_leader_eligible_threshold == 3000.0

def test_config_branch_manager_commission_default():
    config = Config.default()
    assert hasattr(config, 'branch_manager_commission')
    assert len(config.branch_manager_commission.tiers) == 2
    assert config.branch_manager_commission.tiers[0].min_amount == 0
    assert config.branch_manager_commission.tiers[0].max_amount == 50000
    assert config.branch_manager_commission.tiers[0].rate == 0.0
    assert config.branch_manager_commission.tiers[1].min_amount == 50000
    assert config.branch_manager_commission.tiers[1].max_amount is None
    assert config.branch_manager_commission.tiers[1].rate == 0.1

def test_config_branch_manager_eligible_threshold_default():
    config = Config.default()
    assert config.branch_manager_eligible_threshold == 0.0

def test_config_sales_champion_threshold_default():
    config = Config.default()
    assert config.sales_champion_threshold == 20000.0

def test_config_sales_champion_bonus_default():
    config = Config.default()
    assert config.sales_champion_bonus == 500.0