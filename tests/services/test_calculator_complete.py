import pytest
from src.services.calculator import CommissionCalculator
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.models.config import Config

@pytest.fixture
def calculator():
    return CommissionCalculator(Config.default())

@pytest.fixture
def sample_people():
    return {
        "gm": Person(id="gm", name="总主管", performance=5000, role=Role.GENERAL_MANAGER),
        "leader1": Person(id="leader1", name="组长A", performance=5000, role=Role.TEAM_LEADER, group_id="group1"),
        "member1": Person(id="member1", name="成员A1", performance=5000, role=Role.MEMBER, group_id="group1"),
        "member2": Person(id="member2", name="成员A2", performance=3000, role=Role.MEMBER, group_id="group1"),
    }

@pytest.fixture
def sample_groups():
    return {
        "group1": Group(id="group1", name="A组", leader_id="leader1", members=["member1", "member2"])
    }

def test_calculate_person_commission(calculator, sample_people):
    result = calculator.calculate_person(sample_people["member1"])
    assert result.personal_commission == 1000.0
    assert result.management_bonus == 0.0
    assert result.total == result.personal_commission

def test_calculate_leader_commission(calculator, sample_people, sample_groups):
    calculator.set_groups(sample_groups)
    calculator.set_people(sample_people)
    
    result = calculator.calculate_person(sample_people["leader1"])
    assert result.personal_commission == 1000.0
    assert result.team_commission == 1300.0  # (5000+5000+3000达标业绩=13000) * 0.1
    assert result.management_bonus == 200.0  # 2成员 * 100
    assert result.total == 2500.0

def test_calculate_general_manager_commission(calculator, sample_people, sample_groups):
    calculator.set_groups(sample_groups)
    calculator.set_people(sample_people)
    
    result = calculator.calculate_person(sample_people["gm"])
    assert result.personal_commission == 1000.0
    assert result.team_commission == 1800.0  # (5000+5000+5000+3000达标业绩=18000) * 0.1
    assert result.management_bonus == 0.0
    assert result.total == 2800.0