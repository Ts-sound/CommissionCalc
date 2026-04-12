from __future__ import annotations
from dataclasses import dataclass
from typing import List
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

@dataclass
class Config:
    personal_commission: CommissionRule
    team_commission: CommissionRule
    gm_commission: CommissionRule
    temp_leader_commission: CommissionRule
    branch_manager_commission: CommissionRule
    management_bonus_per_person: float
    high_performance_bonuses: List[Bonus]
    eligible_performance_threshold: float
    gm_eligible_threshold: float
    temp_leader_eligible_threshold: float = 3000.0
    branch_manager_eligible_threshold: float = 0.0
    sales_champion_threshold: float = 20000.0
    sales_champion_bonus: float = 500.0
    
    @classmethod
    def default(cls) -> Config:
        return cls(
            personal_commission=CommissionRule(
                rule_type=RuleType.PERSONAL,
                tiers=[
                    Tier(min_amount=0, max_amount=3000, rate=0.0),
                    Tier(min_amount=3000, max_amount=None, rate=0.2)
                ]
            ),
            team_commission=CommissionRule(
                rule_type=RuleType.TEAM,
                tiers=[
                    Tier(min_amount=0, max_amount=10000, rate=0.0),
                    Tier(min_amount=10000, max_amount=50000, rate=0.1),
                    Tier(min_amount=50000, max_amount=None, rate=0.2)
                ]
            ),
            management_bonus_per_person=100.0,
            high_performance_bonuses=[
                Bonus(threshold=20000, amount=500),
                Bonus(threshold=30000, amount=1000),
                Bonus(threshold=50000, amount=2000)
            ],
            eligible_performance_threshold=3000.0,
            gm_commission=CommissionRule(
                rule_type=RuleType.GM,
                tiers=[
                    Tier(min_amount=0, max_amount=50000, rate=0.0),
                    Tier(min_amount=50000, max_amount=None, rate=0.1)
                ]
            ),
            gm_eligible_threshold=50000.0,
            temp_leader_commission=CommissionRule(
                rule_type=RuleType.TEAM,
                tiers=[
                    Tier(min_amount=0, max_amount=10000, rate=0.0),
                    Tier(min_amount=10000, max_amount=50000, rate=0.1),
                    Tier(min_amount=50000, max_amount=None, rate=0.2)
                ]
            ),
            branch_manager_commission=CommissionRule(
                rule_type=RuleType.GM,
                tiers=[
                    Tier(min_amount=0, max_amount=50000, rate=0.0),
                    Tier(min_amount=50000, max_amount=None, rate=0.1)
                ]
            )
        )