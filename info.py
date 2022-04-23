from collections import defaultdict
from copy import deepcopy

class UserInfo:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.sign = ''
        self.loc = ''
        self.fight_num = 0
        self.succ_num = 0
        self.fail_num = 0
        self.get_exp = 0
        self.reward_info = defaultdict(int)
        self.level = 0
        self.ls = 0
        self.bind_ls = 0
        self.xj = 0
        self.hp_store = 0
        self.mp_store = 0
        self.exp = 0
        self.demons = 0 # 心魔
        self.act = 0    # 速力
        self.fairy = 0  # 灵力
        self.team_pwd = ''
        self.team_num = 0
        self.captain_id = 0
        self.is_live = False
        self.in_team = False

missionInfo = {
    'yaoling': {
        'num': 0,
        'loc': '',
        'monster': '',
        'id': 0,
        'succ': False
    },
    'xiangyao': {
        'num': 0,
        'loc': '',
        'monster': '',
        'id': 0,
        'succ': False,
        'run': False,
        'loop_step': 0
    },
    'xunbao': {
        'num': 0,
        'loc': '',
        'monster': '',
        'id': 0,
        'succ': False
    }
}

def createMissionInfo():
    return deepcopy(missionInfo)
