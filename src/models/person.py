from dataclasses import dataclass, field
from typing import Optional, List
from src.models.role import Role

@dataclass
class Person:
    id: str
    name: str
    performance: float = 0.0
    role: Role = Role.MEMBER
    group_id: Optional[str] = None
    managed_groups: List[str] = field(default_factory=list)