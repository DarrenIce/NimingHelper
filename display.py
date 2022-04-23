import re
from datetime import datetime
from collections import defaultdict

import pandas as pd
from rich import box
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, TextColumn, SpinnerColumn, TaskID
from rich.table import Table
from rich.text import Text

from info import UserInfo
from log import Log

logger = Log()()

class GlobalVars:
    program_start_time: datetime = datetime.now()


def make_layout():
    layout = Layout()
    layout.split_row(Layout(name="log", ratio=1), Layout(name="detail", ratio=3))
    layout["detail"].split_column(Layout(name="user", ratio=1))
    return layout

class UserMainInfo:
    def __init__(self, values: list[UserInfo]):
        super().__init__()
        self.values = values

    def __rich__(self) -> Panel:
        info_panel = Panel(
            Group(self.make_team_info(), *self.make_user_status(), self.make_fight_info(), self.make_reward_info()),
            box=box.ROUNDED,
            padding=(1, 1),
            title="队伍监控",
            border_style="bright_blue",
        )
        return info_panel

    def make_team_info(self):
        program_time = pd.to_timedelta(datetime.now() - GlobalVars.program_start_time).ceil('T')
        match_time1 = re.search(r"(\d+)\sdays\s(\d+):(\d+)", str(program_time))
        time1_str = f"{int(match_time1.group(1))}天{int(match_time1.group(2))}小时{int(match_time1.group(3))}分"
        message = Table.grid(expand=True)
        for _ in range(4):
            message.add_column(justify="right")
            message.add_column(justify="left")
        message.add_row("队长:", self.values[0].name,
                        "队伍人数:", str(self.values[0].team_num),
                        "队伍密码:", str(self.values[0].team_pwd),
                        "本队修仙时间:", time1_str)
        return Panel(message, title="队伍信息")

    def make_user_status(self):
        panels = []
        for i in range(len(self.values)):
            message = Table.grid(expand=True)
            for _ in range(7):
                message.add_column(justify="middle")
                message.add_column(justify="left")
            message.add_row("等级:", str(self.values[i].level),
                            "修为:", str(self.values[i].exp),
                            "气血储备:", str(self.values[i].hp_store),
                            "魔法储备:", str(self.values[i].mp_store),
                            "灵力:", str(self.values[i].fairy),
                            "速力:", str(self.values[i].act),
                            "心魔:", str(self.values[i].demons))
            panels.append(Panel(message, title=self.values[i].name))
        return panels

    def make_fight_info(self):
        message = Table.grid(expand=True)
        for _ in range(3):
            message.add_column(justify="right")
            message.add_column(justify="left")
        message.add_row("累计胜利:", str(self.values[0].succ_num),
                        "累计败北:", str(self.values[0].fail_num),
                        "累计修为:", str(self.values[0].get_exp))
        return Panel(message, title="战斗信息")

    def make_reward_info(self):
        rewards = defaultdict(int)
        for i in range(len(self.values)):
            for k in self.values[i].reward_info:
                rewards[k] += self.values[i].reward_info[k]
        message = Text.from_markup('  '.join([f"{k}:{v}" for k, v in rewards.items()]), justify="left")
        return Panel(message, title="奖励信息")


class DynLog:
    log_progress = Progress(SpinnerColumn(), TextColumn("[{task.fields[dt]}] {task.description}"))

    @classmethod
    def record_log(cls, s, error=False):
        task_id = cls.log_progress.add_task("")
        print(f'[{datetime.now().strftime("%H:%M:%S")}]{s}')
        if error:
            logger.error(s)
            cls.log_progress.update(task_id, description=f"[red]{s}", dt=datetime.now().strftime("%H:%M:%S"))
        else:
            logger.info(s)
            cls.log_progress.update(task_id, description=f"[green]{s}", dt=datetime.now().strftime("%H:%M:%S"))
        if task_id >= 1:
            cls.log_progress.update(TaskID(task_id - 1), completed=100)
        if task_id >= 30:
            cls.log_progress.update(TaskID(task_id - 30), visible=False)


class DisplayLayout:
    my_layout = make_layout()
    my_layout["log"].update(Panel(DynLog.log_progress, title="运行日志"))

    @classmethod
    def update_user_info(cls, value):
        cls.my_layout["user"].update(UserMainInfo(values=value))
