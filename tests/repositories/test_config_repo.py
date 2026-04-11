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