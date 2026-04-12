import os
import json
from src.models.config import Config
from src.models.commission import CommissionRule, Tier, RuleType, Bonus

class ConfigRepository:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
    
    def save(self, config: Config):
        config_file = os.path.join(self.config_dir, "settings.json")
        
        data = {
            "personal_commission": {
                "rule_type": config.personal_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.personal_commission.tiers
                ]
            },
            "team_commission": {
                "rule_type": config.team_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.team_commission.tiers
                ]
            },
            "gm_commission": {
                "rule_type": config.gm_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.gm_commission.tiers
                ]
            },
            "temp_leader_commission": {
                "rule_type": config.temp_leader_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.temp_leader_commission.tiers
                ]
            },
            "branch_manager_commission": {
                "rule_type": config.branch_manager_commission.rule_type.value,
                "tiers": [
                    {"min_amount": t.min_amount, "max_amount": t.max_amount, "rate": t.rate}
                    for t in config.branch_manager_commission.tiers
                ]
            },
            "management_bonus_per_person": config.management_bonus_per_person,
            "high_performance_bonuses": [
                {"threshold": b.threshold, "amount": b.amount}
                for b in config.high_performance_bonuses
            ],
            "eligible_performance_threshold": config.eligible_performance_threshold,
            "gm_eligible_threshold": config.gm_eligible_threshold,
            "temp_leader_eligible_threshold": config.temp_leader_eligible_threshold,
            "branch_manager_eligible_threshold": config.branch_manager_eligible_threshold,
            "sales_champion_threshold": config.sales_champion_threshold,
            "sales_champion_bonus": config.sales_champion_bonus
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> Config:
        config_file = os.path.join(self.config_dir, "settings.json")
        
        if not os.path.exists(config_file):
            return Config.default()
        
        with open(config_file, encoding='utf-8') as f:
            data = json.load(f)
        
        return Config(
            personal_commission=CommissionRule(
                rule_type=RuleType(data["personal_commission"]["rule_type"]),
                tiers=[
                    Tier(**t) for t in data["personal_commission"]["tiers"]
                ]
            ),
            team_commission=CommissionRule(
                rule_type=RuleType(data["team_commission"]["rule_type"]),
                tiers=[
                    Tier(**t) for t in data["team_commission"]["tiers"]
                ]
            ),
            gm_commission=CommissionRule(
                rule_type=RuleType(data.get("gm_commission", {}).get("rule_type", "总主管团队提成")),
                tiers=[
                    Tier(**t) for t in data.get("gm_commission", {}).get("tiers", [
                        {"min_amount": 0, "max_amount": 50000, "rate": 0.0},
                        {"min_amount": 50000, "max_amount": None, "rate": 0.1}
                    ])
                ]
            ),
            temp_leader_commission=CommissionRule(
                rule_type=RuleType(data.get("temp_leader_commission", {}).get("rule_type", "团队业绩提成")),
                tiers=[
                    Tier(**t) for t in data.get("temp_leader_commission", {}).get("tiers", [
                        {"min_amount": 0, "max_amount": 10000, "rate": 0.0},
                        {"min_amount": 10000, "max_amount": 50000, "rate": 0.1},
                        {"min_amount": 50000, "max_amount": None, "rate": 0.2}
                    ])
                ]
            ),
            branch_manager_commission=CommissionRule(
                rule_type=RuleType(data.get("branch_manager_commission", {}).get("rule_type", "总主管团队提成")),
                tiers=[
                    Tier(**t) for t in data.get("branch_manager_commission", {}).get("tiers", [
                        {"min_amount": 0, "max_amount": 50000, "rate": 0.0},
                        {"min_amount": 50000, "max_amount": None, "rate": 0.1}
                    ])
                ]
            ),
            management_bonus_per_person=data["management_bonus_per_person"],
            high_performance_bonuses=[
                Bonus(**b) for b in data["high_performance_bonuses"]
            ],
            eligible_performance_threshold=data.get("eligible_performance_threshold", 3000.0),
            gm_eligible_threshold=data.get("gm_eligible_threshold", 50000.0),
            temp_leader_eligible_threshold=data.get("temp_leader_eligible_threshold", 3000.0),
            branch_manager_eligible_threshold=data.get("branch_manager_eligible_threshold", 0.0),
            sales_champion_threshold=data.get("sales_champion_threshold", 20000.0),
            sales_champion_bonus=data.get("sales_champion_bonus", 500.0)
        )