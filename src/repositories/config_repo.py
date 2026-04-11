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
            "management_bonus_per_person": config.management_bonus_per_person,
            "high_performance_bonuses": [
                {"threshold": b.threshold, "amount": b.amount}
                for b in config.high_performance_bonuses
            ]
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
            management_bonus_per_person=data["management_bonus_per_person"],
            high_performance_bonuses=[
                Bonus(**b) for b in data["high_performance_bonuses"]
            ]
        )