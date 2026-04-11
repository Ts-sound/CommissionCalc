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