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

def test_calculate_general_manager_commission(sample_people, sample_groups):
    config = Config.default()
    config.gm_eligible_threshold = 3000.0
    calculator = CommissionCalculator(config)
    
    sample_people["gm"].performance = 50000
    sample_people["leader1"].performance = 50000
    sample_people["member1"].performance = 50000
    sample_people["member2"].performance = 30000
    
    calculator.set_groups(sample_groups)
    calculator.set_people(sample_people)
    
    result = calculator.calculate_person(sample_people["gm"])
    assert result.team_commission == 18000.0  # (50000+50000+50000+30000达标业绩=180000) * 0.1

def test_gm_team_commission_with_gm_threshold():
    config = Config.default()
    config.gm_eligible_threshold = 50000.0
    
    calculator = CommissionCalculator(config)
    
    gm = Person(id="gm", name="总主管", role=Role.GENERAL_MANAGER, performance=60000)
    leader = Person(id="l1", name="组长", role=Role.TEAM_LEADER, performance=20000)
    member = Person(id="m1", name="成员", role=Role.MEMBER, performance=40000)
    
    calculator.set_people({gm.id: gm, leader.id: leader, member.id: member})
    calculator.set_groups({})
    
    result = calculator.calculate_person(gm)
    
    assert result.team_commission == 6000.0

def test_gm_team_commission_multiple_eligible():
    config = Config.default()
    config.gm_eligible_threshold = 30000.0
    
    calculator = CommissionCalculator(config)
    
    gm = Person(id="gm", name="总主管", role=Role.GENERAL_MANAGER, performance=60000)
    leader = Person(id="l1", name="组长", role=Role.TEAM_LEADER, performance=40000)
    member = Person(id="m1", name="成员", role=Role.MEMBER, performance=50000)
    
    calculator.set_people({gm.id: gm, leader.id: leader, member.id: member})
    calculator.set_groups({})
    
    result = calculator.calculate_person(gm)
    
    assert result.team_commission == 15000.0

def test_temp_leader_team_commission_excludes_self():
    config = Config.default()
    config.temp_leader_eligible_threshold = 3000.0
    calculator = CommissionCalculator(config)
    
    temp_leader = Person(id="tl1", name="临时组长", role=Role.TEMP_LEADER, performance=20000, group_id="group1")
    member_a = Person(id="m1", name="成员A", role=Role.MEMBER, performance=40000, group_id="group1")
    member_b = Person(id="m2", name="成员B", role=Role.MEMBER, performance=2000, group_id="group1")
    
    group = Group(id="group1", name="A组", leader_id="leader1", members=["m1", "m2"])
    
    calculator.set_people({temp_leader.id: temp_leader, member_a.id: member_a, member_b.id: member_b, "leader1": Person(id="leader1", name="组长", role=Role.TEAM_LEADER, performance=5000)})
    calculator.set_groups({"group1": group})
    
    result = calculator.calculate_person(temp_leader)
    
    assert result.team_commission == 4000.0

def test_branch_manager_team_commission():
    config = Config.default()
    config.branch_manager_eligible_threshold = 0.0
    calculator = CommissionCalculator(config)
    
    bm = Person(id="bm", name="分主管", role=Role.BRANCH_MANAGER, performance=60000, managed_groups=["group1", "group2"])
    leader1 = Person(id="l1", name="组长A", role=Role.TEAM_LEADER, performance=40000, group_id="group1")
    leader2 = Person(id="l2", name="组长B", role=Role.TEAM_LEADER, performance=30000, group_id="group2")
    member_a1 = Person(id="m_a1", name="成员A1", role=Role.MEMBER, performance=20000, group_id="group1")
    member_b1 = Person(id="m_b1", name="成员B1", role=Role.MEMBER, performance=15000, group_id="group2")
    
    group1 = Group(id="group1", name="A组", leader_id="l1", members=["m_a1"])
    group2 = Group(id="group2", name="B组", leader_id="l2", members=["m_b1"])
    
    calculator.set_people({bm.id: bm, leader1.id: leader1, leader2.id: leader2, member_a1.id: member_a1, member_b1.id: member_b1})
    calculator.set_groups({"group1": group1, "group2": group2})
    
    result = calculator.calculate_person(bm)
    
    assert result.team_commission == 16500.0

def test_sales_champion_bonus():
    config = Config.default()
    config.sales_champion_threshold = 20000.0
    config.sales_champion_bonus = 500.0
    calculator = CommissionCalculator(config)
    
    person_a = Person(id="a", name="A", role=Role.MEMBER, performance=50000)
    person_b = Person(id="b", name="B", role=Role.MEMBER, performance=30000)
    person_c = Person(id="c", name="C", role=Role.MEMBER, performance=15000)
    
    calculator.set_people({person_a.id: person_a, person_b.id: person_b, person_c.id: person_c})
    calculator.set_groups({})
    
    results = calculator.calculate_all()
    
    assert results["a"].sales_champion_bonus == 500.0
    assert results["b"].sales_champion_bonus == 0.0
    assert results["c"].sales_champion_bonus == 0.0

def test_no_sales_champion_below_threshold():
    config = Config.default()
    config.sales_champion_threshold = 20000.0
    config.sales_champion_bonus = 500.0
    calculator = CommissionCalculator(config)
    
    person_a = Person(id="a", name="A", role=Role.MEMBER, performance=15000)
    person_b = Person(id="b", name="B", role=Role.MEMBER, performance=10000)
    person_c = Person(id="c", name="C", role=Role.MEMBER, performance=5000)
    
    calculator.set_people({person_a.id: person_a, person_b.id: person_b, person_c.id: person_c})
    calculator.set_groups({})
    
    results = calculator.calculate_all()
    
    assert results["a"].sales_champion_bonus == 0.0
    assert results["b"].sales_champion_bonus == 0.0
    assert results["c"].sales_champion_bonus == 0.0

def test_commission_rate_calculation():
    calculator = CommissionCalculator(Config.default())
    
    person = Person(id="p1", name="成员", role=Role.MEMBER, performance=5000)
    
    result = calculator.calculate_person(person)
    
    assert result.commission_rate == 0.2