import pytest
from src.models.role import Role

def test_role_values():
    assert Role.GENERAL_MANAGER.value == "总主管"
    assert Role.TEAM_LEADER.value == "正式组长"
    assert Role.MEMBER.value == "成员"

def test_role_count():
    assert len(Role) == 5

def test_branch_manager_role():
    assert hasattr(Role, 'BRANCH_MANAGER')
    assert Role.BRANCH_MANAGER.value == "分主管"

def test_temp_leader_role():
    assert hasattr(Role, 'TEMP_LEADER')
    assert Role.TEMP_LEADER.value == "临时组长"