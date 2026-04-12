from enum import Enum

class Role(Enum):
    GENERAL_MANAGER = "总主管"
    BRANCH_MANAGER = "分主管"
    TEAM_LEADER = "正式组长"
    TEMP_LEADER = "临时组长"
    MEMBER = "成员"