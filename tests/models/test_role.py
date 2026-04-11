import pytest
from src.models.role import Role

def test_role_values():
    assert Role.GENERAL_MANAGER.value == "总主管"
    assert Role.TEAM_LEADER.value == "组长"
    assert Role.MEMBER.value == "成员"

def test_role_count():
    assert len(Role) == 3