from src.models.commission import CommissionRule

def calculate_personal_commission(performance: float, rule: CommissionRule) -> float:
    if performance <= 0:
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= performance:
            if tier.max_amount is None or performance < tier.max_amount:
                return performance * tier.rate
    
    return 0.0