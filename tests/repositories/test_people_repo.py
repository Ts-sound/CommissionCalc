import pytest
import os
import json
import tempfile
from src.repositories.people_repo import PeopleRepository
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def people_repo(temp_dir):
    return PeopleRepository(temp_dir)

def test_save_and_load_empty(people_repo):
    people, groups = people_repo.load()
    assert len(people) == 0
    assert len(groups) == 0

def test_save_and_load_people(people_repo):
    person = Person(id="p1", name="张三", role=Role.MEMBER)
    people = {"p1": person}
    groups = {}
    
    people_repo.save(people, groups)
    
    loaded_people, loaded_groups = people_repo.load()
    assert len(loaded_people) == 1
    assert loaded_people["p1"].name == "张三"
    assert loaded_people["p1"].role == Role.MEMBER

def test_save_and_load_groups(people_repo):
    group = Group(id="g1", name="A组", leader_id="l1", members=["m1", "m2"])
    groups = {"g1": group}
    people = {}
    
    people_repo.save(people, groups)
    
    loaded_people, loaded_groups = people_repo.load()
    assert len(loaded_groups) == 1
    assert loaded_groups["g1"].name == "A组"
    assert loaded_groups["g1"].leader_id == "l1"
    assert len(loaded_groups["g1"].members) == 2
    assert "m1" in loaded_groups["g1"].members
    assert "m2" in loaded_groups["g1"].members

def test_save_and_load_managed_groups(people_repo):
    branch_manager = Person(
        id="bm1",
        name="分主管张",
        role=Role.BRANCH_MANAGER,
        managed_groups=["g1", "g2"]
    )
    people = {"bm1": branch_manager}
    groups = {"g1": Group(id="g1", name="A组", leader_id=None), "g2": Group(id="g2", name="B组", leader_id=None)}
    
    people_repo.save(people, groups)
    
    loaded_people, _ = people_repo.load()
    assert loaded_people["bm1"].managed_groups == ["g1", "g2"]

def test_load_missing_managed_groups_defaults_to_empty(people_repo):
    people_json = '''
    {
        "people": [{"id": "p1", "name": "张三", "role": "成员"}],
        "groups": []
    }
    '''
    import json
    with open(people_repo.people_file, 'w', encoding='utf-8') as f:
        f.write(people_json)
    
    loaded_people, _ = people_repo.load()
    assert loaded_people["p1"].managed_groups == []

def test_load_old_config_without_managed_groups(people_repo):
    people_json = '''
    {
        "people": [
            {"id": "bm1", "name": "分主管", "role": "分主管", "group_id": null}
        ],
        "groups": []
    }
    '''
    import json
    with open(people_repo.people_file, 'w', encoding='utf-8') as f:
        f.write(people_json)
    
    loaded_people, _ = people_repo.load()
    assert loaded_people["bm1"].managed_groups == []

def test_save_and_load_full_structure(people_repo):
    leader = Person(id="l1", name="组长", role=Role.TEAM_LEADER, group_id="g1")
    member1 = Person(id="m1", name="成员1", role=Role.MEMBER, group_id="g1")
    member2 = Person(id="m2", name="成员2", role=Role.MEMBER, group_id="g1")
    
    group = Group(id="g1", name="A组", leader_id="l1", members=["m1", "m2"])
    
    people = {"l1": leader, "m1": member1, "m2": member2}
    groups = {"g1": group}
    
    people_repo.save(people, groups)
    
    loaded_people, loaded_groups = people_repo.load()
    
    assert len(loaded_people) == 3
    assert len(loaded_groups) == 1
    
    loaded_group = loaded_groups["g1"]
    assert loaded_group.name == "A组"
    assert loaded_group.leader_id == "l1"
    assert len(loaded_group.members) == 2
    assert "m1" in loaded_group.members
    assert "m2" in loaded_group.members