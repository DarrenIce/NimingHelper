# 匿名修仙助手

## 功能

- [x] 自动挂机
  - [x] 断线重连
  - [x] 整队挂机
  - [x] 加入其他队伍挂机
- [x] 每日任务
  - [x] 采药
  - [x] 寻宝
  - [x] 降妖 
    - [x] 降妖目前只支持多角色组队进行，队长自动释放平纹金阳
    - [ ] 暂不支持加入其他队伍进行降妖

## 已知问题

- 每日任务战斗失败会导致卡住

## 运行环境

需要你有一个python(仅在python3.9、3.10测试通过)，还需要你有多个代理端口(同Ip超过两个用户将无法进行每日任务)

### 安装MiniConda
```
curl -O https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
sh Miniconda3-py39_4.11.0-Linux-x86_64.sh
```

### 配置运行环境
```
conda create -n niming python=3.9
conda activate niming
cd NimingHelper
pip install -r requirements.txt
cp config_example.yml config.yml
vim config.yml
```

### 运行
```
python main.py
```

## 注意事项
最多支持填入5个账号，第一个账号将作为降妖和挂机的队长，第一个技能将作为每个人进行采药和寻宝的自动技能