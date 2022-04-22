from ws import WSocket
from common import moveto
from display import DynLog

import time
import requests
import json


# 打药灵之前先组队、开自动再开始
class YaoLing:
    start_loc = "丹城"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始药灵任务")
        for i in range(10 - ws.missioninfo.yaoling_num):
            moveto(ws, ws.userinfo.loc, cls.start_loc)
            is_take = False
            while True:
                try:
                    r = requests.post('https://game.nimingxx.com/api/task/join', data={'type': 'cy'}, cookies={"sign": ws.userinfo.sign, "niming_email": ws.username}, proxies=proxies)
                    ms_info = json.loads(r.text)
                    if ms_info['code'] == 200:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        is_take = True
                        ws.missioninfo.yaoling_succ = False
                        DynLog.record_log(f"{ws.userinfo.name}接取第{ws.missioninfo.yaoling_num + i + 1}次药灵任务")
                        break
                    else:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        if '未完成' in ms_info['msg']:
                            is_take = True
                            break
                        is_take = False
                        return
                except requests.exceptions.SSLError as e:
                    DynLog.record_log(ws.userinfo.name + "药灵任务接取失败，重试...", True)
            if is_take:
                ws.send('{"msgType":"task_refesh"}')
                time.sleep(2)
                moveto(ws, cls.start_loc, ws.missioninfo.yaoling_loc)
                DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo.yaoling_monster}")
                ws.fight(ws.missioninfo.yaoling_id)
                time.sleep(2)
                while not ws.missioninfo.yaoling_succ:
                    time.sleep(1)
                DynLog.record_log(f"{ws.userinfo.name}完成第{ws.missioninfo.yaoling_num + i + 1}次药灵任务")
        DynLog.record_log(f"{ws.userinfo.name}完成药灵任务")

class XiangYao:
    start_loc = "林中栈道"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始降妖任务")
        for i in range(3 - ws.missioninfo.xiangyao_num):
            pass
        DynLog.record_log(f"{ws.userinfo.name}完成降妖任务")
               
class XunBao:
    start_loc = "阳城"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始寻宝任务")
        for i in range(10 - ws.missioninfo.xunbao_num):
            moveto(ws, ws.userinfo.loc, cls.start_loc)
            is_take = False
            while True:
                try:
                    r = requests.post('https://game.nimingxx.com/api/task/join', data={'type': 'bt'}, cookies={"sign": ws.userinfo.sign, "niming_email": ws.username}, proxies=proxies)
                    ms_info = json.loads(r.text)
                    if ms_info['code'] == 200:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        is_take = True
                        ws.missioninfo.xunbao_succ = False
                        DynLog.record_log(f"{ws.userinfo.name}接取第{ws.missioninfo.xunbao_num + i + 1}次寻宝任务")
                        break
                    else:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        if '未完成' in ms_info['msg']:
                            is_take = True
                            break
                        is_take = False
                        return
                except requests.exceptions.SSLError as e:
                    DynLog.record_log(ws.userinfo.name + "寻宝任务接取失败，重试...", True)
            if is_take:
                ws.send('{"msgType":"task_refesh"}')
                time.sleep(2)
                ws.fly(ws.missioninfo.xunbao_loc)
                time.sleep(2)
                DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo.xunbao_monster}")
                ws.fight(ws.missioninfo.xunbao_id)
                time.sleep(2)
                while not ws.missioninfo.xunbao_succ:
                    time.sleep(1)
                DynLog.record_log(f"{ws.userinfo.name}完成第{ws.missioninfo.xunbao_num + i + 1}次寻宝任务")
        DynLog.record_log(f"{ws.userinfo.name}完成寻宝任务")