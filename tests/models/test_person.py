import pytest
from src.models.person import Person
from src.models.role import Role

def test_person_creation():
    person = Person(
        id="test-id",
        name="张三",
        performance=5000.0,
        role=Role.TEAM_LEADER,
        group_id="group-1"
    )
    assert person.id == "test-id"
    assert person.name == "张三"
    assert person.performance == 5000.0
    assert person.role == Role.TEAM_LEADER
    assert person.group_id == "group-1"

def test_person_optional_group():
    person = Person(
        id="gm-id",
        name="总主管",
        performance=10000.0,
        role=Role.GENERAL_MANAGER
    )
    assert person.group_id is None

def test_person_default_performance():
    person = Person(
        id="member-id",
        name="成员",
        role=Role.MEMBER
    )
    assert person.performance == 0.0

def test_person_managed_groups_default():
    person = Person(
        id="bm-id",
        name="分主管",
        role=Role.BRANCH_MANAGER
    )
    assert person.managed_groups == []

def test_person_managed_groups_multiple():
    person = Person(
        id="bm-id",
        name="分主管",
        role=Role.BRANCH_MANAGER,
        managed_groups=["group-1", "group-2", "group-3"]
    )
    assert person.managed_groups == ["group-1", "group-2", "group-3"]