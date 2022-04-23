from info import UserInfo, createMissionInfo
from display import DynLog
from common import moveto

import requests
import json
import time
import websocket
import threading
import os

# websocket.enableTrace(True)

headers = {
    'Host': 'game.nimingxx.com'
}

WS_URL = "wss://game.nimingxx.com/ws?sign="
LOGIN_API = "https://game.nimingxx.com/api/login"

class WSocket:
    def __init__(self, username, password, proxy_host, proxy_port):
        self.userinfo = UserInfo()
        self.missioninfo = createMissionInfo()
        self.username = username
        self.password = password
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.ws = None

    def login(self):
        if self.proxy_host:
            self.proxies = {
                "http": f"http://{self.proxy_host}:{self.proxy_port}",
                "https": f"http://{self.proxy_host}:{self.proxy_port}"
            }
        else:
            self.proxies = {}
        login_info = {}
        while True:
            try:
                r = requests.post(LOGIN_API, headers=headers, data={"loginName": self.username, "loginPwd": self.password}, proxies=self.proxies)
                if r.status_code == 200:
                    login_info = json.loads(r.text)
                    break
            except requests.exceptions.SSLError as e:
                DynLog.record_log('request failed, retry...', True)
        # print(r.status_code)
        while r.status_code != 200 or login_info['code'] != 200:
            r = requests.post(LOGIN_API, headers=headers, data={"loginName": self.username, "loginPwd": self.password}, proxies=self.proxies)
            # print(r.text)
            DynLog.record_log(f'{self.username} retry login...', True)
            if r.status_code == 200:
                login_info = json.loads(r.text)
            time.sleep(10)
        self.userinfo.name = login_info['data']['role']['name']
        self.userinfo.id = login_info['data']['role']['auto_id']
        self.userinfo.sign = login_info['data']['sign']
        self.userinfo.loc = login_info['data']['role']['d']
        self.signn(self.proxies)
        self.fetchActivityInfo(self.proxies)
        self.ws = websocket.WebSocketApp(WS_URL + self.userinfo.sign, on_message=self.on_message)
        self.wsthread = threading.Thread(target=self.ws.run_forever, args=[None, None, 60, None, '{"msgType":"ping"}', self.proxy_host, self.proxy_port, None, None, False, None, None, None, False, "http"])
        self.wsthread.start()
        time.sleep(3)
        # self.ws.run_forever(ping_interval=60, ping_payload=json.dumps({"msgType":"ping"}), http_proxy_host=PROXY_HOST, http_proxy_port=PROXY_PORT, proxy_type="http")
        try:
            self.send(json.dumps({
                "msgType": "login",
                "id": 1,
                "sign": self.userinfo.sign,
            }))
            time.sleep(2)
        except:
            return
        # self.send('{"msgType":"ref_role"}')
        self.rfthread = threading.Thread(target=self.refreshInfo)
        self.rfthread.start()
        self.userinfo.is_live = True
        # self.closeLog()

    def signn(self, PROXY):
        while True:
            try:
                r = requests.post("https://game.nimingxx.com/api/role/sign", headers=headers, cookies={"sign": self.userinfo.sign, "niming_email": self.username}, proxies=PROXY)
                DynLog.record_log(self.userinfo.name + json.loads(r.text)['msg'])
                r = requests.post("https://game.nimingxx.com/api/role/receiveWhReward", headers=headers, cookies={"sign": self.userinfo.sign, "niming_email": self.username}, proxies=PROXY)
                DynLog.record_log(self.userinfo.name + json.loads(r.text)['msg'])
                return
            except requests.exceptions.SSLError as e:
                DynLog.record_log(f'{self.userinfo.name} sign failed, retry...', True)
            

    def fetchActivityInfo(self, PROXY):
        while True:
            try:
                r = requests.post("https://game.nimingxx.com/api/role/getActivity", headers=headers, cookies={"sign": self.userinfo.sign, "niming_email": self.username}, proxies=PROXY)
                DynLog.record_log(self.userinfo.name + " 获取每日任务信息")
                msg = json.loads(r.text)
                self.missioninfo['yaoling']['num'] = msg['data']['cy']
                self.missioninfo['xiangyao']['num'] = msg['data']['xy']
                self.missioninfo['xunbao']['num'] = msg['data']['xb']
                return
            except requests.exceptions.SSLError as e:
                DynLog.record_log(f'{self.userinfo.name} fetchActivityInfo failed, retry...', True)


    def on_message(self, wsapp, message):
        msg = json.loads(message)
        if msg['msgId'] == 'team_create':
            self.userinfo.team_pwd = msg['data']['Pwd']
            self.userinfo.in_team = True
            DynLog.record_log(f'{self.userinfo.name}创建队伍成功, 密令: {self.userinfo.team_pwd}')
        elif msg['msgId'] == 'ref_role':
            self.userinfo.level = msg['data']['level'] if 'level' in msg['data'] else self.userinfo.level
            self.userinfo.ls = msg['data']['ls'] if 'ls' in msg['data'] else self.userinfo.ls
            self.userinfo.bind_ls = msg['data']['bind_ls'] if 'bind_ls' in msg['data'] else self.userinfo.bind_ls
            self.userinfo.xj = msg['data']['xj'] if 'xj' in msg['data'] else self.userinfo.xj
            self.userinfo.hp_store = int(msg['data']['hp_store']) if 'hp_store' in msg['data'] else self.userinfo.hp_store
            self.userinfo.mp_store = int(msg['data']['mp_store']) if 'mp_store' in msg['data'] else self.userinfo.mp_store
            self.userinfo.exp = msg['data']['exp'] if 'exp' in msg['data'] else self.userinfo.exp
            self.userinfo.demons = msg['data']['demons'] if 'demons' in msg['data'] else self.userinfo.demons
            self.userinfo.act = msg['data']['act'] if 'act' in msg['data'] else self.userinfo.act
            self.userinfo.fairy = msg['data']['fairy'] if 'fairy' in msg['data'] else self.userinfo.fairy

            if self.userinfo.hp_store < 10000:
                self.exchange_lingqi(1, 10000)
            if self.userinfo.mp_store < 10000:
                self.exchange_lingqi(2, 10000)
            if self.userinfo.act < 100:
                self.exchange_lingqi(3, 5000)
        elif msg['msgId'] == 'move':
            DynLog.record_log(f'{self.userinfo.name}移动到' + msg['data']['map'])
            self.userinfo.loc = msg['data']['map']
            for scene in msg['data']['scenes']:
                if scene['name'] == self.missioninfo['yaoling']['monster']:
                    self.missioninfo['yaoling']['id'] = scene['id']
                    DynLog.record_log(f"{self.missioninfo['yaoling']['monster']}ID为{self.missioninfo['yaoling']['id']}")
                if scene['name'] == self.missioninfo['xunbao']['monster']:
                    self.missioninfo['xunbao']['id'] = scene['id']
                    DynLog.record_log(f"{self.missioninfo['xunbao']['monster']}ID为{self.missioninfo['xunbao']['id']}")
                if scene['name'] == self.missioninfo['xiangyao']['monster']:
                    self.missioninfo['xiangyao']['id'] = scene['id']
                    self.missioninfo['xiangyao']['run'] = False
                    DynLog.record_log(f"{self.missioninfo['xiangyao']['monster']}ID为{self.missioninfo['xiangyao']['id']}")
        elif msg['msgId'] == 'team_move':
            DynLog.record_log(f'{self.userinfo.name}随队伍移动到' + msg['data']['map'])
        elif msg['msgId'] == 'bat_round_result':
            self.userinfo.fight_num += 1
            if 'lose' not in msg['data']:
                pass
            else:
                if msg['data']['lose'] == 1:
                    DynLog.record_log(f'{self.userinfo.name}战斗失败', True)
                    self.userinfo.fail_num += 1
                else:
                    self.userinfo.succ_num += 1
                    good_txt = ''
                    if 'exp' in msg['m']:
                        self.userinfo.get_exp += msg['m']['exp']
                    if 'rewards' in msg['m']:
                        good_txt = "，获得"
                        for good in msg['m']['rewards']:
                            good_txt = good_txt + f"{good['name']}*{good['num']}"
                            self.userinfo.reward_info[good['name']] += good['num']
                        DynLog.record_log(f'{self.userinfo.name}战斗胜利' + good_txt)
                tnt = ''
                for u in msg['data']['round_arr']:
                    tnt = tnt + f"{u['name']}-{u['process']} "
                if self.userinfo.team_pwd != '':
                    DynLog.record_log(tnt)
        elif msg['msgId'] == 'bat_start_result':
            pass
        elif msg['msgId'] == 'login':
            DynLog.record_log(f'{msg["connId"]}登录成功')
        elif msg['msgId'] == 'team_refresh':
            self.userinfo.team_num = msg['data']['Count']
        elif msg['msgId'] == 'team_list':
            for team in msg['data']:
                if team['Id'] == self.userinfo.id:
                    self.userinfo.team_num = team['Count']
                    break
        elif msg['msgId'] == 'warning':
            DynLog.record_log(f'{self.userinfo.name}: {msg["msg"]}')
        elif msg['msgId'] == 'success':
            DynLog.record_log(f'{self.userinfo.name}: {msg["msg"]}')
        elif msg['msgId'] == 'chat':
            pass
        elif msg['msgId'] == 'task_refesh':
            for task in msg['data']:
                # DynLog.record_log(task)
                if 'info' in task['task'] and '药灵' in task['task']['info']:
                    self.missioninfo['yaoling']['loc'] = task['d']
                    self.missioninfo['yaoling']['monster'] = task['scenes'][0]['name']
                    DynLog.record_log(f"{self.missioninfo['yaoling']['monster']}在{self.missioninfo['yaoling']['loc']}")
                elif 'info' in task['task'] and '寻宝' in task['task']['info']:
                    self.missioninfo['xunbao']['loc'] = task['d']
                    self.missioninfo['xunbao']['monster'] = task['scenes'][0]['name']
                    DynLog.record_log(f"{self.missioninfo['xunbao']['monster']}在{self.missioninfo['xunbao']['loc']}")
                elif 'name' in task['task'] and task['task']['name'] == '降妖':
                    self.missioninfo['xiangyao']['loc'] = task['d']
                    self.missioninfo['xiangyao']['monster'] = task['scenes'][0]['name']
                    DynLog.record_log(f"{self.missioninfo['xiangyao']['monster']}在{self.missioninfo['xiangyao']['loc']}")
        elif msg['msgId'] == 'complete_task':
            if '药灵' in msg['data']['task']['name']:
                self.missioninfo['yaoling']['succ'] = True
            elif '寻宝' in msg['data']['task']['name']:
                self.missioninfo['xunbao']['succ'] = True
        elif msg['msgId'] == 'ref_task':
            if 'msg' in msg and self.missioninfo['xiangyao']['monster'] in msg['msg']:
                for task in msg['role_tasks']:
                    if task['task']['name'] == '降妖':
                        self.missioninfo['xiangyao']['run'] = True
                        self.missioninfo['xiangyao']['loop_step'] = task['loop_step']
            if 'msg' in msg and '完成[降妖]' in msg['msg']:
                self.missioninfo['xiangyao']['succ'] = True
                self.missioninfo['xiangyao']['loop_step'] = 11
        elif msg['msgId'] == 'ch_leave':
            DynLog.record_log(f"{msg['connId']}离开了队伍")
            if msg['connId'] == self.userinfo.captain_id:
                self.userinfo.in_team = False
        else:
            DynLog.record_log(message)

    def closeLog(self):
        self.send(json.dumps({"msgType":"close_log","off": True}))

    def move(self, dest):
        self.send(json.dumps({"msgType":"move","d": dest,"t":""}))

    def fly(self, dest):
        self.send(json.dumps({"msgType":"move","d": dest,"t":"10"}))

    def fight(self, monster_id):
        self.send(json.dumps({"msgType":"scene_bat","mid": monster_id}))

    def fight_cycle(self, mname):
        monsters = {}
        with open('monsters.json', 'r', encoding='utf-8') as f:
            monsters = json.load(f)
        mid = monsters[mname]['id']
        while True:
            if self.userinfo.demons > 1000:
                DynLog.record_log(f'{self.userinfo.name}心魔过高，退出', True)
                os._exit(0)
            self.send(json.dumps({"msgType":"scene_bat","mid": mid}))
            time.sleep(2.5)

    def exchange_lingqi(self, lid, llnum):
        # 1 - 加血
        # 2 - 加蓝
        # 3 - 速力
        n2c_dct = {
            1: '气血储备',
            2: '魔法储备',
            3: '速力',
        }
        self.send(json.dumps({
            'msgType': 'role_poly',
            'type': str(lid),
            'num': llnum,
        }))
        time.sleep(2)
        if lid == 1 or lid == 2:
            DynLog.record_log(f"{self.userinfo.name}增加{n2c_dct[lid]} {llnum * 50}点")
        else:
            DynLog.record_log(f"{self.userinfo.name}增加{n2c_dct[lid]} {int(llnum / 50)}点")

    def goto_monster(self, mname):
        monsters = {}
        with open('monsters.json', 'r', encoding='utf-8') as f:
            monsters = json.load(f)
        monster_dest = monsters[mname]['map']
        moveto(self, self.userinfo.loc, monster_dest)

    def createTeam(self):
        self.send('{"msgType":"team_create","is_pwd":true}')
        time.sleep(2)

    def joinTeam(self, captain_id, team_pwd):
        self.send(json.dumps({"msgType":"team_add","tid":captain_id,"pwd":team_pwd}))
        self.userinfo.captain_id = captain_id
        time.sleep(2)

    def leaveTeam(self):
        self.send('{"msgType":"team_leave"}')
        time.sleep(2)

    def refreshTeam(self):
        self.send('{"msgType":"team_refresh"}')
        time.sleep(2)

    def setAutoFight(self, skill):
        skills = {}
        with open('skills.json', 'r', encoding='utf-8') as f:
            skills = json.load(f)
        self.send(json.dumps({"msgType":"bat_auto_skill","sid":skills[skill],"auto": True}))
        DynLog.record_log(f'{self.userinfo.name}设置自动技能为{skill}')
        time.sleep(2)

    def refreshInfo(self):
        while True:
            self.send('{"msgType":"ref_role"}')
            time.sleep(2)
            if self.userinfo.team_pwd != '':
                self.send('{"msgType":"team_list"}')
                time.sleep(2)
            time.sleep(30)

    def send(self, payload):
        try:
            self.ws.send(payload)
        except websocket._exceptions.WebSocketConnectionClosedException as e:
            DynLog.record_log(f'{self.userinfo.name}连接已断开', True)
            self.userinfo.is_live = False
            self.rfthread.join()