from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from src.models.commission import CommissionRule, Bonus
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.models.config import Config

@dataclass
class CommissionResult:
    person_id: str
    personal_commission: float = 0.0
    team_commission: float = 0.0
    management_bonus: float = 0.0
    high_performance_bonus: float = 0.0
    total: float = 0.0

class CommissionCalculator:
    def __init__(self, config: Config):
        self.config = config
        self.people: Dict[str, Person] = {}
        self.groups: Dict[str, Group] = {}
    
    def set_people(self, people: Dict[str, Person]):
        self.people = people
    
    def set_groups(self, groups: Dict[str, Group]):
        self.groups = groups
    
    def calculate_person(self, person: Person) -> CommissionResult:
        result = CommissionResult(person_id=person.id)
        
        result.personal_commission = calculate_personal_commission(
            person.performance, self.config.personal_commission
        )
        
        if person.role in [Role.TEAM_LEADER, Role.GENERAL_MANAGER]:
            result.team_commission = self._calculate_team_commission(person)
        
        if person.role == Role.TEAM_LEADER:
            result.management_bonus = self._calculate_management_bonus(person)
        
        result.high_performance_bonus = calculate_high_performance_bonus(
            person.performance, self.config.high_performance_bonuses
        )
        
        result.total = (
            result.personal_commission +
            result.team_commission +
            result.management_bonus +
            result.high_performance_bonus
        )
        
        return result
    
    def _calculate_team_commission(self, person: Person) -> float:
        threshold = self.config.eligible_performance_threshold
        
        if person.role == Role.GENERAL_MANAGER:
            team_performance = sum(
                p.performance for p in self.people.values() 
                if p.performance >= threshold
            )
        else:
            group = self.groups.get(person.group_id)
            if group:
                team_performance = 0.0
                
                leader = self.people.get(group.leader_id)
                if leader and leader.performance >= threshold:
                    team_performance += leader.performance
                
                for mid in group.members:
                    if mid in self.people:
                        member = self.people[mid]
                        if member.performance >= threshold:
                            team_performance += member.performance
            else:
                team_performance = 0.0
        
        return calculate_team_commission(team_performance, self.config.team_commission)
    
    def _calculate_management_bonus(self, person: Person) -> float:
        group = self.groups.get(person.group_id)
        if group:
            return calculate_management_bonus(
                len(group.members), self.config.management_bonus_per_person
            )
        return 0.0

def calculate_personal_commission(performance: float, rule: CommissionRule) -> float:
    if performance <= 0:
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= performance:
            if tier.max_amount is None or performance < tier.max_amount:
                return performance * tier.rate
    
    return 0.0

def calculate_team_commission(team_performance: float, rule: CommissionRule) -> float:
    if team_performance <= 0:
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= team_performance:
            if tier.max_amount is None or team_performance < tier.max_amount:
                return team_performance * tier.rate
    
    return 0.0

def calculate_management_bonus(member_count: int, bonus_per_person: float) -> float:
    return member_count * bonus_per_person

def calculate_high_performance_bonus(performance: float, bonuses: List[Bonus]) -> float:
        for bonus in reversed(bonuses):
            if performance >= bonus.threshold:
                return bonus.amount
        return 0.0