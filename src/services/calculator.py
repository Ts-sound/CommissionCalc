from typing import List
from src.models.commission import CommissionRule, Bonus

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
    total_bonus = 0.0
    for bonus in bonuses:
        if performance >= bonus.threshold:
            total_bonus += bonus.amount
    return total_bonus