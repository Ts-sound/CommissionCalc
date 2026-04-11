from dataclasses import dataclass, field
from typing import List

@dataclass
class Group:
    id: str
    name: str
    leader_id: str
    members: List[str] = field(default_factory=list)
    
    def add_member(self, member_id: str):
        if member_id not in self.members:
            self.members.append(member_id)
    
    def remove_member(self, member_id: str):
        if member_id in self.members:
            self.members.remove(member_id)