import pytest
from src.services.calculator import CommissionResult

def test_commission_result_default_values():
    result = CommissionResult(person_id="test-id")
    assert result.personal_commission == 0.0
    assert result.team_commission == 0.0
    assert result.management_bonus == 0.0
    assert result.high_performance_bonus == 0.0
    assert result.total == 0.0
    assert result.sales_champion_bonus == 0.0
    assert result.commission_rate == 0.0

def test_commission_result_sales_champion_bonus():
    result = CommissionResult(
        person_id="test-id",
        sales_champion_bonus=500.0
    )
    assert result.sales_champion_bonus == 500.0

def test_commission_result_commission_rate():
    result = CommissionResult(
        person_id="test-id",
        commission_rate=0.2
    )
    assert result.commission_rate == 0.2