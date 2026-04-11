import pytest
from src.models.group import Group

def test_group_creation():
    group = Group(
        id="group-1",
        name="A组",
        leader_id="leader-1",
        members=["member-1", "member-2"]
    )
    assert group.id == "group-1"
    assert group.name == "A组"
    assert group.leader_id == "leader-1"
    assert group.members == ["member-1", "member-2"]

def test_group_default_members():
    group = Group(
        id="group-2",
        name="B组",
        leader_id="leader-2"
    )
    assert group.members == []

def test_add_member():
    group = Group(id="g1", name="Group", leader_id="l1", members=[])
    group.add_member("m1")
    assert "m1" in group.members

def test_remove_member():
    group = Group(id="g1", name="Group", leader_id="l1", members=["m1", "m2"])
    group.remove_member("m1")
    assert "m1" not in group.members
    assert "m2" in group.members