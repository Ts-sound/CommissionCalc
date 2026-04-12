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

def test_save_load_temp_leader_commission(config_repo):
    config = Config.default()
    config_repo.save(config)
    
    loaded_config = config_repo.load()
    assert hasattr(loaded_config, 'temp_leader_commission')
    assert len(loaded_config.temp_leader_commission.tiers) == 3
    assert loaded_config.temp_leader_commission.tiers[0].rate == 0.0
    assert loaded_config.temp_leader_commission.tiers[1].rate == 0.1
    assert loaded_config.temp_leader_commission.tiers[2].rate == 0.2

def test_save_load_branch_manager_commission(config_repo):
    config = Config.default()
    config_repo.save(config)
    
    loaded_config = config_repo.load()
    assert hasattr(loaded_config, 'branch_manager_commission')
    assert len(loaded_config.branch_manager_commission.tiers) == 2
    assert loaded_config.branch_manager_commission.tiers[1].rate == 0.1

def test_save_load_new_thresholds(config_repo):
    config = Config.default()
    config_repo.save(config)
    
    loaded_config = config_repo.load()
    assert loaded_config.temp_leader_eligible_threshold == 3000.0
    assert loaded_config.branch_manager_eligible_threshold == 0.0
    assert loaded_config.sales_champion_threshold == 20000.0
    assert loaded_config.sales_champion_bonus == 500.0

def test_backward_compatibility_missing_new_fields(config_repo):
    old_data = {
        "personal_commission": {
            "rule_type": "个人业绩提成",
            "tiers": [
                {"min_amount": 0, "max_amount": 3000, "rate": 0.0},
                {"min_amount": 3000, "max_amount": None, "rate": 0.2}
            ]
        },
        "team_commission": {
            "rule_type": "团队业绩提成",
            "tiers": [
                {"min_amount": 0, "max_amount": 10000, "rate": 0.0},
                {"min_amount": 10000, "max_amount": 50000, "rate": 0.1},
                {"min_amount": 50000, "max_amount": None, "rate": 0.2}
            ]
        },
        "gm_commission": {
            "rule_type": "总主管团队提成",
            "tiers": [
                {"min_amount": 0, "max_amount": 50000, "rate": 0.0},
                {"min_amount": 50000, "max_amount": None, "rate": 0.1}
            ]
        },
        "management_bonus_per_person": 100.0,
        "high_performance_bonuses": [
            {"threshold": 20000, "amount": 500},
            {"threshold": 30000, "amount": 1000},
            {"threshold": 50000, "amount": 2000}
        ],
        "eligible_performance_threshold": 3000.0,
        "gm_eligible_threshold": 50000.0
    }
    
    config_file = os.path.join(config_repo.config_dir, "settings.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)
    
    loaded_config = config_repo.load()
    assert loaded_config.temp_leader_eligible_threshold == 3000.0
    assert loaded_config.branch_manager_eligible_threshold == 0.0
    assert loaded_config.sales_champion_threshold == 20000.0
    assert loaded_config.sales_champion_bonus == 500.0