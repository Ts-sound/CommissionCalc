from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from src.models.commission import CommissionRule, Bonus
from src.models.person import Person
from src.models.group import Group
from src.models.role import Role
from src.models.config import Config
from src.utils.logger import get_logger

logger = get_logger()

@dataclass
class CommissionResult:
    person_id: str
    personal_commission: float = 0.0
    team_commission: float = 0.0
    management_bonus: float = 0.0
    high_performance_bonus: float = 0.0
    sales_champion_bonus: float = 0.0
    commission_rate: float = 0.0
    total: float = 0.0

class CommissionCalculator:
    def __init__(self, config: Config):
        self.config = config
        self.people: Dict[str, Person] = {}
        self.groups: Dict[str, Group] = {}
        logger.debug(f"初始化提成计算器，达标线={config.eligible_performance_threshold}")
    
    def set_people(self, people: Dict[str, Person]):
        self.people = people
        logger.debug(f"设置人员数据，共{len(people)}人")
    
    def set_groups(self, groups: Dict[str, Group]):
        self.groups = groups
        logger.debug(f"设置组别数据，共{len(groups)}组")
    
    def calculate_person(self, person: Person) -> CommissionResult:
        logger.info(f"======== 计算提成: {person.name} ========")
        logger.debug(f"  业绩={person.performance}, 身份={person.role.value}, 组别={person.group_id}")
        
        result = CommissionResult(person_id=person.id)
        
        result.personal_commission = calculate_personal_commission(
            person.performance, self.config.personal_commission
        )
        logger.debug(f"  个人提成={result.personal_commission}")
        
        if person.role in [Role.TEAM_LEADER, Role.GENERAL_MANAGER]:
            result.team_commission = self._calculate_team_commission(person)
            logger.debug(f"  团队提成={result.team_commission}")
        
        if person.role == Role.TEAM_LEADER:
            result.management_bonus = self._calculate_management_bonus(person)
            logger.debug(f"  管理提成={result.management_bonus}")
        
        result.high_performance_bonus = calculate_high_performance_bonus(
            person.performance, self.config.high_performance_bonuses
        )
        logger.debug(f"  高业绩奖金={result.high_performance_bonus}")
        
        result.total = (
            result.personal_commission +
            result.team_commission +
            result.management_bonus +
            result.high_performance_bonus
        )
        
        logger.info(f"  总提成={result.total}")
        
        return result
    
    def _calculate_team_commission(self, person: Person) -> float:
        if person.role == Role.GENERAL_MANAGER:
            threshold = self.config.gm_eligible_threshold
            commission_rule = self.config.gm_commission
            logger.debug(f"  计算总主管团队提成，达标线={threshold}")
            
            eligible_people = [p for p in self.people.values() if p.performance >= threshold]
            logger.debug(f"  达标人数={len(eligible_people)}/{len(self.people)}")
            
            for p in eligible_people:
                logger.debug(f"    {p.name}: {p.performance} (达标)")
            
            team_performance = sum(p.performance for p in eligible_people)
            logger.debug(f"  团队总业绩={team_performance}")
        else:
            threshold = self.config.eligible_performance_threshold
            commission_rule = self.config.team_commission
            logger.debug(f"  计算团队提成，达标线={threshold}")
            
            group = self.groups.get(person.group_id)
            if group:
                logger.debug(f"  组长团队业绩计算开始，组别={group.name}")
                team_performance = 0.0
                
                leader = self.people.get(group.leader_id)
                if leader:
                    if leader.performance >= threshold:
                        team_performance += leader.performance
                        logger.debug(f"    组长{leader.name}: {leader.performance} (达标)")
                    else:
                        logger.debug(f"    组长{leader.name}: {leader.performance} (未达标)")
                
                for mid in group.members:
                    if mid in self.people:
                        member = self.people[mid]
                        if member.performance >= threshold:
                            team_performance += member.performance
                            logger.debug(f"    成员{member.name}: {member.performance} (达标)")
                        else:
                            logger.debug(f"    成员{member.name}: {member.performance} (未达标)")
                
                logger.debug(f"  组内达标业绩合计={team_performance}")
            else:
                logger.warning(f"  组长{person.name}未找到组别配置")
                team_performance = 0.0
        
        commission = calculate_team_commission(team_performance, commission_rule)
        logger.debug(f"  团队提成={commission}")
        return commission
    
    def _calculate_management_bonus(self, person: Person) -> float:
        group = self.groups.get(person.group_id)
        if group:
            member_count = len(group.members)
            logger.debug(f"  管理提成计算，组员数={member_count}")
            return calculate_management_bonus(
                member_count, self.config.management_bonus_per_person
            )
        logger.warning(f"  组长{person.name}未找到组别配置，管理提成=0")
        return 0.0

def calculate_personal_commission(performance: float, rule: CommissionRule) -> float:
    if performance <= 0:
        logger.debug(f"    个人提成计算: 业绩={performance}, 结果=0 (业绩为0)")
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= performance:
            if tier.max_amount is None or performance < tier.max_amount:
                commission = performance * tier.rate
                logger.debug(f"    个人提成计算: 业绩={performance}, 匹配阶梯[{tier.min_amount}-{tier.max_amount or '∞'}], 比例={tier.rate}, 结果={commission}")
                return commission
    
    logger.debug(f"    个人提成计算: 业绩={performance}, 结果=0 (无匹配阶梯)")
    return 0.0

def calculate_team_commission(team_performance: float, rule: CommissionRule) -> float:
    if team_performance <= 0:
        logger.debug(f"    团队提成计算: 团队业绩={team_performance}, 结果=0 (业绩为0)")
        return 0.0
    
    for tier in rule.tiers:
        if tier.min_amount <= team_performance:
            if tier.max_amount is None or team_performance < tier.max_amount:
                commission = team_performance * tier.rate
                logger.debug(f"    团队提成计算: 团队业绩={team_performance}, 匹配阶梯[{tier.min_amount}-{tier.max_amount or '∞'}], 比例={tier.rate}, 结果={commission}")
                return commission
    
    logger.debug(f"    团队提成计算: 团队业绩={team_performance}, 结果=0 (无匹配阶梯)")
    return 0.0

def calculate_management_bonus(member_count: int, bonus_per_person: float) -> float:
    bonus = member_count * bonus_per_person
    logger.debug(f"    管理提成计算: 成员数={member_count}, 每人={bonus_per_person}, 结果={bonus}")
    return bonus

def calculate_high_performance_bonus(performance: float, bonuses: List[Bonus]) -> float:
    logger.debug(f"    高业绩奖金计算: 业绩={performance}")
    for bonus in reversed(bonuses):
        logger.debug(f"      检查阈值={bonus.threshold}, 奖金={bonus.amount}")
        if performance >= bonus.threshold:
            logger.debug(f"      匹配阈值={bonus.threshold}, 结果={bonus.amount}")
            return bonus.amount
    logger.debug(f"      无匹配阈值, 结果=0")
    return 0.0