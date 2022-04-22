# 匿名修仙助手

## 功能
- [x] 自动挂机
  - [x] 断线重连
  - [x] 整队挂机
- [x] 每日任务
  - [x] 采药
  - [x] 寻宝
  - [ ] 降妖 

## 运行环境
需要你有一个python(仅在python3.9、3.10测试通过)，还需要你有多个代理端口(同Ip超过两个用户将无法进行每日任务)

## 启动
pip install -r requirements.txt
以config_example.yml为模板，创建config.yml文件，最多支持填入5个账号，第一个账号将作为降妖和挂机的队长，第一个技能将作为每个人进行采药和寻宝的自动技能

python main.py即可启动