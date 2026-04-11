import os
import json
from typing import Dict
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role

class PeopleRepository:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
        self.people_file = os.path.join(config_dir, "people.json")
    
    def load(self) -> tuple[Dict[str, Person], Dict[str, Group]]:
        people = {}
        groups = {}
        
        if not os.path.exists(self.people_file):
            return people, groups
        
        with open(self.people_file, encoding='utf-8') as f:
            data = json.load(f)
        
        for group_data in data.get("groups", []):
            group = Group(
                id=group_data["id"],
                name=group_data["name"],
                leader_id=group_data.get("leader_id"),
                members=group_data.get("members", [])
            )
            groups[group.id] = group
        
        for person_data in data.get("people", []):
            person = Person(
                id=person_data["id"],
                name=person_data["name"],
                role=Role(person_data["role"]),
                group_id=person_data.get("group_id")
            )
            people[person.id] = person
        
        return people, groups
    
    def save(self, people: Dict[str, Person], groups: Dict[str, Group]):
        data = {
            "people": [
                {
                    "id": p.id,
                    "name": p.name,
                    "role": p.role.value,
                    "group_id": p.group_id
                }
                for p in people.values()
            ],
            "groups": [
                {
                    "id": g.id,
                    "name": g.name,
                    "leader_id": g.leader_id,
                    "members": g.members
                }
                for g in groups.values()
            ]
        }
        
        with open(self.people_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)