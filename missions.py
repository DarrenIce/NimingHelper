from turtle import pos
from ws import WSocket
from common import moveto
from display import DynLog

import time
import requests
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

class YaoLing:
    start_loc = "丹城"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始药灵任务")
        for i in range(10 - ws.missioninfo['yaoling']['num']):
            moveto(ws, ws.userinfo.loc, cls.start_loc)
            is_take = False
            while True:
                try:
                    r = requests.post('https://game.nimingxx.com/api/task/join', headers=headers, data={'type': 'cy'}, cookies={"sign": ws.userinfo.sign, "niming_email": ws.username}, proxies=proxies)
                    ms_info = json.loads(r.text)
                    if ms_info['code'] == 200:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        is_take = True
                        ws.missioninfo['yaoling']['succ'] = False
                        DynLog.record_log(f"{ws.userinfo.name}接取第{ws.missioninfo['yaoling']['num'] + i + 1}次药灵任务")
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
                moveto(ws, cls.start_loc, ws.missioninfo['yaoling']['loc'])
                time.sleep(2)
                DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo['yaoling']['monster']}")
                ws.fight(ws.missioninfo['yaoling']['id'])
                time.sleep(2)
                while not ws.missioninfo['yaoling']['succ']:
                    time.sleep(1)
                DynLog.record_log(f"{ws.userinfo.name}完成第{ws.missioninfo['yaoling']['num'] + i + 1}次药灵任务")
        DynLog.record_log(f"{ws.userinfo.name}完成药灵任务")

class XiangYao:
    start_loc = "林中栈道"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始降妖任务")
        maps = []
        with open('map.json', 'r', encoding='utf-8') as a:
            maps = json.loads(a.read())
        for i in range(3 - ws.missioninfo['xiangyao']['num'] + 1):
            moveto(ws, ws.userinfo.loc, cls.start_loc)
            is_take = False
            while True:
                try:
                    r = requests.post('https://game.nimingxx.com/api/task/join', headers=headers, data={'type': 'xy'}, cookies={"sign": ws.userinfo.sign, "niming_email": ws.username}, proxies=proxies)
                    ms_info = json.loads(r.text)
                    if ms_info['code'] == 200:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        is_take = True
                        ws.missioninfo['xiangyao']['succ'] = False
                        DynLog.record_log(f"{ws.userinfo.name}接取第{ws.missioninfo['xiangyao']['num'] + i + 1}次降妖任务")
                        break
                    else:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        if '未完成' in ms_info['msg']:
                            is_take = True
                            break
                        is_take = False
                        return
                except requests.exceptions.SSLError as e:
                    DynLog.record_log(ws.userinfo.name + "降妖任务接取失败，重试...", True)
            if is_take:
                ws.missioninfo['xiangyao']['succ'] = False
                ws.missioninfo['xiangyao']['run'] = False
                ws.missioninfo['xiangyao']['loop_step'] = 0
                ws.send('{"msgType":"task_refesh"}')
                time.sleep(2)
                moveto(ws, cls.start_loc, ws.missioninfo['xiangyao']['loc'])
                time.sleep(3)
                DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo['xiangyao']['monster']}")
                ws.fight(ws.missioninfo['xiangyao']['id'])
                base_loc = ws.userinfo.loc
                time.sleep(4)
                while ws.missioninfo['xiangyao']['loop_step'] <= 10:
                    while not ws.missioninfo['xiangyao']['run']:
                        time.sleep(1)
                    possible_locs = maps[base_loc]
                    for ploc in possible_locs:
                        ws.move(ploc)
                        time.sleep(4)
                        if not ws.missioninfo['xiangyao']['run']:
                            break
                        else:
                            ws.move(base_loc)
                            time.sleep(2)
                    DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo['xiangyao']['monster']}")
                    ws.fight(ws.missioninfo['xiangyao']['id'])
                    base_loc = ws.userinfo.loc
                while not ws.missioninfo['xiangyao']['succ']:
                    time.sleep(1)
                DynLog.record_log(f"{ws.userinfo.name}完成第{ws.missioninfo['xiangyao']['num'] + i + 1}次降妖任务")
        DynLog.record_log(f"{ws.userinfo.name}完成降妖任务")
               
class XunBao:
    start_loc = "阳城"

    @classmethod
    def run(cls, ws: WSocket, proxies):
        DynLog.record_log(f"{ws.userinfo.name}开始寻宝任务")
        for i in range(10 - ws.missioninfo['xunbao']['num']):
            moveto(ws, ws.userinfo.loc, cls.start_loc)
            is_take = False
            while True:
                try:
                    r = requests.post('https://game.nimingxx.com/api/task/join', headers=headers, data={'type': 'bt'}, cookies={"sign": ws.userinfo.sign, "niming_email": ws.username}, proxies=proxies)
                    ms_info = json.loads(r.text)
                    if ms_info['code'] == 200:
                        DynLog.record_log(ws.userinfo.name + ms_info['msg'])
                        is_take = True
                        ws.missioninfo['xunbao']['succ'] = False
                        DynLog.record_log(f"{ws.userinfo.name}接取第{ws.missioninfo['xunbao']['num'] + i + 1}次寻宝任务")
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
                ws.fly(ws.missioninfo['xunbao']['loc'])
                time.sleep(4)
                DynLog.record_log(f"{ws.userinfo.name}对战{ws.missioninfo['xunbao']['monster']}")
                ws.fight(ws.missioninfo['xunbao']['id'])
                time.sleep(2)
                while not ws.missioninfo['xunbao']['succ']:
                    time.sleep(1)
                DynLog.record_log(f"{ws.userinfo.name}完成第{ws.missioninfo['xunbao']['num'] + i + 1}次寻宝任务")
        DynLog.record_log(f"{ws.userinfo.name}完成寻宝任务")