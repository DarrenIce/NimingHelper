from collections import deque
import json
import time

maps = {}
with open('map.json', 'r', encoding='utf-8') as f:
    maps = json.load(f)

def search_widest(start,target):
    if start == target:
        return []
    parent_node = {}
    searched = [start] # 已经搜索过的顶点
    search_queue = deque() # 搜索队列
    search_queue += maps[start]
    for area in maps[start]:
        parent_node[area] = start
    while search_queue:
        v = search_queue.popleft() # 出队一个待搜索顶点
        if v in searched or v not in maps.keys():
            continue
        searched.append(v)
        if v == target:
            break
        else:
            search_queue += maps[v] # 待搜索顶点搜索队列
            for area in maps[v]:
                if area not in parent_node:
                    parent_node[area] = v
    path = target
    node = target
    steps = [target]
    while node != start:
        node = parent_node[node]
        path = node + '-->' + path
        steps.append(node)
    steps.pop()
    steps.reverse()
    # print('搜索 %s -> %s 最短路径'%(start,target))
    # print(path)
    # print(steps)
    return steps


def moveto(ws, start, target):
    steps = search_widest(start, target)
    if len(steps) < 5:
        for step in steps:
            ws.move(step)
            time.sleep(2)
    else:
        ws.fly(target)
        time.sleep(2)