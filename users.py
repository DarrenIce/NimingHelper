import threading
import time
import os

from display import DynLog, DisplayLayout
from missions import *
from ws import WSocket

class Users:
    def __init__(self, conf):
        self.conf = conf
        self.wss: list[WSocket] = []

    def login(self):
        for i in range(len(self.conf.get('users', {}).get('username', []))):
            wss = WSocket(self.conf.get('users', {}).get('username', [])[i],
                          self.conf.get('users', {}).get('password', [])[i],
                          self.conf.get('proxy', {}).get('host', ''),
                          self.conf.get('proxy', {}).get('port', [k for k in range(len(self.conf.get('users', {}).get('username', [])))])[i])
            wss.login()
            self.wss.append(wss)

    def ready(self):
        for i in range(len(self.wss)):
            self.wss[i].goto_monster(self.conf.get('fight', {}).get('monster', ''))
            if i == 0:
                self.wss[i].createTeam()
            else:
                captain_id = self.wss[0].userinfo.id
                team_pwd = self.wss[0].userinfo.team_pwd
                self.wss[i].joinTeam(captain_id, team_pwd)
                self.wss[i].userinfo.in_team = True
            self.wss[i].setAutoFight(self.conf.get('fight', {}).get('skill', [])[i])

    def do_missions(self):
        for i in self.conf.get('mission', {}).get('id', []):
            if i == 1 or i == 2:
                for ws in self.wss:
                    ws.createTeam()
                    ws.setAutoFight(self.conf.get('fight', {}).get('skill', [])[0])
                    if i == 1:
                        YaoLing.run(ws, ws.proxies)
                    elif i == 2:
                        XunBao.run(ws, ws.proxies)
                    ws.leaveTeam()

    def fight(self):
        try:
            monsters = {}
            with open('monsters.json', 'r', encoding='utf-8') as f:
                monsters = json.load(f)
            mid = monsters[self.conf.get('fight', {}).get('monster', '')]['id']
            while True:
                if self.wss[0].userinfo.demons > 1000:
                    DynLog.record_log(f'{self.wss[0].userinfo.name}心魔过高，退出', True)
                    os._exit(0)
                self.wss[0].send(json.dumps({"msgType":"scene_bat","mid": mid}))
                time.sleep(2.5)
        except Exception as e:
            DynLog.record_log(e, True)
            os._exit(0)

    def run(self):
        self.uithread = threading.Thread(target=self.updateInfos)
        self.uithread.start()
        self.do_missions()
        self.ready()
        self.fthread = threading.Thread(target=self.fight)
        self.fthread.start()
        time.sleep(120)
        self.lcthread = threading.Thread(target=self.liveCheck)
        self.lcthread.start()
        threading.Thread(target=self.threadCheck).start()

    def updateInfos(self):
        while True:
            try:
                infos = []
                for i in range(len(self.wss)):
                    infos.append(self.wss[i].userinfo)
                DisplayLayout.update_user_info(infos)
                time.sleep(10)
            except Exception as e:
                DynLog.record_log(e, True)

    def liveCheck(self):
        while True:
            for i in range(len(self.wss)):
                if not self.wss[i].userinfo.is_live:
                    DynLog.record_log(self.wss[i].userinfo.name + "尝试重连", True)
                    wss = WSocket(self.conf.get('users', {}).get('username', [])[i],
                          self.conf.get('users', {}).get('password', [])[i],
                          self.conf.get('proxy', {}).get('host', ''),
                          self.conf.get('proxy', {}).get('port', [])[i])
                    wss.login()
                    self.wss[i] = wss
                    if i == 0:
                        self.wss[i].createTeam()
                        self.wss[i].setAutoFight(self.conf.get('fight', {}).get('skill', [])[i])
                        threading.Thread(target=self.fight).start()
                    else:
                        if self.wss[0].userinfo.in_team:
                            captain_id = self.wss[0].userinfo.id
                            team_pwd = self.wss[0].userinfo.team_pwd
                            self.wss[i].joinTeam(captain_id, team_pwd)
                            self.wss[i].userinfo.in_team = True
                            self.wss[i].setAutoFight(self.conf.get('fight', {}).get('skill', [])[i])
                        else:
                            self.wss[i].userinfo.in_team = False
                elif not self.wss[i].userinfo.in_team and i != 0:
                    if self.wss[0].userinfo.in_team:
                        captain_id = self.wss[0].userinfo.id
                        team_pwd = self.wss[0].userinfo.team_pwd
                        self.wss[i].joinTeam(captain_id, team_pwd)
                        self.wss[i].userinfo.in_team = True
                        self.wss[i].setAutoFight(self.conf.get('fight', {}).get('skill', [])[i])
            time.sleep(10)

    def threadCheck(self):
        while True:
            if not self.uithread.is_alive():
                self.uithread = threading.Thread(target=self.updateInfos)
                self.uithread.start()
            if not self.fthread.is_alive():
                self.fthread = threading.Thread(target=self.fight)
                self.fthread.start()
            if not self.lcthread.is_alive():
                self.lcthread = threading.Thread(target=self.liveCheck)
                self.lcthread.start()
            time.sleep(10)