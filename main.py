# -*- coding: utf-8 -*-
# @Time : 2022/1/23 20:41
# @Author : zzy
# @File : main
# @Description :

import json
import threading
import time
import requests as requests
from bilibili_api import sync, video


def get_cid(bvid: str) -> str:
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取信息
    info = sync(v.get_info())  # 同步执行异步代码
    # 打印信息
    return info['cid']


def print_total_number():
    global cid,args
    timer = threading.Timer(int(args.interval), print_total_number)
    timer.start()
    url = 'http://api.bilibili.com/x/player/online/total'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
    }
    params = {"bvid": args.bvid, 'cid': cid}
    e = requests.get(url, headers=headers, params=params)  # 当前网站链接
    html = e.content.decode('utf-8')
    json_data = json.loads(html)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:-3]
    print(current_time + ' , ' + json_data['data']['total'])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("获取bilibili视频的实时在线人数")
    parser.add_argument('bvid',help="视频的BV号")
    parser.add_argument('interval',help="检测实时在线人数的时间间隔（秒）")
    args = parser.parse_args()
    cid = get_cid(args.bvid)
    print_total_number()
