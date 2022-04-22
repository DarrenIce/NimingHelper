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
        self.reward_info = {}
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
        self.is_live = False
        self.in_team = False

class MissionInfo:
    def __init__(self):
        self.yaoling_num = 0
        self.yaoling_loc = ''
        self.yaoling_monster = ''
        self.yaoling_id = 0
        self.yaoling_succ = False
        self.xiangyao_num = 0
        self.xiangyao_loc = ''
        self.xiangyao_monster = ''
        self.xiangyao_id = 0
        self.xiangyao_succ = False
        self.xunbao_num = 0
        self.xunbao_loc = ''
        self.xunbao_monster = ''
        self.xunbao_id = 0
        self.xunbao_succ = False