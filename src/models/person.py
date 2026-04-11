from dataclasses import dataclass
from typing import Optional
from src.models.role import Role

@dataclass
class Person:
    id: str
    name: str
    performance: float = 0.0
    role: Role = Role.MEMBER
    group_id: Optional[str] = None