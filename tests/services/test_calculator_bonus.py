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
    assert calculate_high_performance_bonus(30000, bonuses) == 1000.0

def test_bonus_35000(bonuses):
    assert calculate_high_performance_bonus(35000, bonuses) == 1000.0

def test_bonus_at_50000(bonuses):
    assert calculate_high_performance_bonus(50000, bonuses) == 2000.0

def test_bonus_55000(bonuses):
    assert calculate_high_performance_bonus(55000, bonuses) == 2000.0

def test_bonus_empty_list():
    assert calculate_high_performance_bonus(30000, []) == 0.0