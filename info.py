from collections import defaultdict, deque
from functools import partial
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
        self.info_deque = defaultdict(partial(deque, maxlen=128))
        self.estimate_info = {}
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

def format_string_num(s: str) -> str:
    sign = np.sign(int(s))
    num = abs(int(s))
    if num >= 1e4:
        return f'{sign * num / 1e4:.1f}万/小时'
    else:
        return f'{sign * num:.1f}/小时'

def estimate_info(deq):
    df = pd.DataFrame(deq)
    df['time'] = pd.to_datetime(df.time)
    df.set_index('time', inplace=True)
    df = df.loc[datetime.now() - timedelta(minutes=20):datetime.now()]
    if df.shape[0] < 5:
        return {}
    df_diff = df.diff(axis=0).dropna(how='all')
    df_diff["exp"] = df_diff.exp.where(df_diff.exp >= 0, df_diff.exp.median())
    df_diff["hp_store"] = df_diff.hp_store.where(df_diff.hp_store <= 0, df_diff.hp_store.median())
    df_diff["mp_store"] = df_diff.mp_store.where(df_diff.mp_store <= 0, df_diff.mp_store.median())
    deque_sec = (df_diff.index[-1] - df_diff.index[0]).total_seconds()
    estimate_result = (df_diff.sum() / deque_sec * 3600)
    estimate = estimate_result.apply(format_string_num)
    return estimate.to_dict()
