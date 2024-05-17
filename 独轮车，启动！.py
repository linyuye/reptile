#偶尔发多了就需要验证码，等一会就行，要么延长发送时间
#林宇叶 2024/5/17
#仅作为学习使用

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
import hashlib
import time
from urllib.parse import quote
import re
import pytz
import json
import datetime
import random
from fake_useragent import UserAgent
ua=UserAgent()#创立随机请求头

headers = {
            'User-Agent': ua.random,
            'Cookie': "",

}
url = "https://api.bilibili.com/x/v2/reply/add"
message = "把你要发的内容写在这里面"
initial_data = {
        'type': '17',#https://github.com/SocialSisterYi/bilibili-API-collect/
        'message' : message,
        'oid' : '',
        'csrf' : '你的csrf，从cookie里面找bili_jct写进来',
        'plat': '1'
        }
# 1	视频稿件	稿件 avid
# 2	话题	话题 id
# 4	活动	活动 id
# 5	小视频	小视频 id
# 6	小黑屋封禁信息	封禁公示 id
# 7	公告信息	公告 id
# 8	直播活动	直播间 id
# 9	活动稿件	(?)
# 10	直播公告	(?)
# 11	相簿（图片动态）	相簿 id
# 12	专栏	专栏 cvid
# 13	票务	(?)
# 14	音频	音频 auid
# 15	风纪委员会	众裁项目 id
# 16	点评	(?)
# 17	动态（纯文字动态&分享）	动态 id
# 18	播单	(?)
# 19	音乐播单	(?)
# 20	漫画	(?)
# 21	漫画	(?)
# 22	漫画	漫画 mcid
# 33	课程	课程 epid
def add_random_number_to_message(original_message):
     # 生成一个随机数字（比如1-100之间）
     random_number = random.randint(1, 100)
     # 构造新的message，后面添加随机数字
     new_message = f"{original_message}{random_number}"
     return new_message
#调用函数，并更新data字典中的message字段
#函数作用，在你写的内容后面加一个数字发出去，如果要发别的内容可以自己构造message列表
for i in range(100):
    data = {**initial_data, 'message': add_random_number_to_message(message)}
    with requests.Session() as session:
            retries = Retry(total=3,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))
            response = session.post(url, data=data, headers=headers)
            # 检查响应
            print(f"第{i + 1}次请求的状态码：", response.status_code)
            print(response.text)
            pause_time = random.uniform(3, 5)
            print(f"为了规避发的太快被屏蔽，正在暂停 {pause_time:.2f} 秒...")
            time.sleep(pause_time)  # 暂停指定的秒数
