# B站评论分页爬取，可以实现动态，视频，转发动态的无限爬取
# api来源 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/comment/list.md
# 感谢api来源
# 作者：林宇叶 2024/5/1
# 本软件仅限于个人学习使用，请在下载后的24小时内删除
# 使用内容时，请遵守网站robots守则，不要对网站进行破坏性挖掘
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
import hashlib
import time
from urllib.parse import quote
import re
import pytz
import datetime
from fake_useragent import UserAgent
import random

# 重试次数限制
MAX_RETRIES = 5
# 重试间隔（秒）
RETRY_INTERVAL = 5

# 用户名密码方式,填写后需要注释
# 基于代理ip网站，新用户给24小时试用
# 代理ip来源：https://www.kuaidaili.com/free/inha/
"""
username = ""
password = ""
tunnel = ""
"""


beijing_tz = pytz.timezone('Asia/Shanghai')  # 时间戳转换为北京时间
ua = UserAgent()  # 创立随机请求头
"""
在这里修改你爬取页码的参数，使用前取消注释
oid = 
type =   # 类型 11个人动态 17转发动态 视频1）
ps =   # (每页含有条数，不能大于20)用long的话不能大于30
down =   # 开始爬的页数
up =   # 结束爬的页数

在这里修改你爬取页码的参数
"""
one_comments = []
all_comments = []  # 构造数据放在一起的容器  总共评论，如果只希望含有一级评论，请注释 line 141
#即all_comments.append([name, sex, formatted_time, like, message, location, count])
all_2_comments = []  # 构造数据放在一起的容器 二级评论

with requests.Session() as session:
    retries = Retry(total=3,  # 最大重试次数，好像没有这个函数
                    backoff_factor=0.1,  # 间隔时间会乘以这个数
                    status_forcelist=[500, 502, 503, 504])

    for page in range(down, up + 1):
        for retry in range(MAX_RETRIES):
            try:
                headers = {
                    'User-Agent': ua.random,  # 随机请求头，b站爸爸别杀我，赛博佛祖保佑
                    'Cookie': '',}            #你的cookie
                url = 'https://api.bilibili.com/x/v2/reply?'  # 正常api，只能爬8k
                url_long = 'https://api.bilibili.com/x/v2/reply/main'  # 懒加载api，理论无上限
                url_reply = 'https://api.bilibili.com/x/v2/reply/reply'  # 评论区回复api
                # 示例：https://api.bilibili.com/x/v2/reply/main?next=1&type=1&oid=544588138&mode=3（可访问网站）
                data = {
                    # 其余没写懒加载api的均为正常api
                    'next': str(page),  # 页数，需要转换为字符串，与pn同理，使用懒加载api
                    # 'pn': str(page),  # 页数，需要转换为字符串
                    'type': type,  # 类型 11个人动态 17转发动态 视频1）
                    'oid': oid,  # id，视频为av，文字动态地址栏id，可自查
                    'ps': ps,  # (每页含有条数，不能大于20)用long的话不能大于30
                    # 'sort': '0'  # 排序方式，0最新（即查看时间排序），1历史（看最先发言的），2为热度 34没发现有什么用
                    'mode': '3'  # 3为热度       0 3：仅按热度      1：按热度+按时间 2：仅按时间 使用懒加载api
                    # mid =  uid 想查询某个人发言看这个mid
                    # count 二级评论所含有的数量 > 0对其构造二级评论
                    # pn 二级评论页数，需要转换为字符串
                }
                proxies = {
                    #代理ip，防被杀
                }
                prep = session.prepare_request(requests.Request('GET', url_long, params=data, headers=headers))
                print(prep.url)
                response = session.get(url_long, params=data, headers=headers, proxies=proxies)
                # 检查响应状态码是否为200，即成功
                if response.status_code == 200:
                    json_data = response.json()  # 获得json数据
                    if 'data' in json_data and 'replies' in json_data['data']:  # 以下为核心内容，爬取的数据
                        for comment in json_data['data']['replies']:
                            one_comments.clear()
                            count = comment['count']
                            rpid = comment['rpid'] #评论的身份，类似于uuid，为下方检测二级评论
                            name = comment['member']['uname']
                            sex = comment['member']['sex']
                            ctime = comment['ctime']
                            # 使用datetime.fromtimestamp和datetime.timezone.utc来创建UTC时间的datetime对象
                            dt_object = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc)
                            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S') + ' 北京时间'  # 可以加上时区信息，但通常不需要
                            like = comment['like']
                            message = comment['content']['message'].replace('\n', ',')
                            # 检查是否存在 location 字段
                            location = comment['reply_control'].get('location', '未知')  # 如果不存在，使用 '未知'
                            location = location.replace('IP属地：', '') if location else location
                            # 将提取的信息追加到列表中
                            # one_comments.append([name, sex, formatted_time, like, message, location])#理论作废，每爬一次就输进去一次，防止爬虫被杀
                            all_comments.append([name, sex, formatted_time, like, message, location, count])
                            # 每次结束，重置计数器
                            if (count != 0):
                                print(f"在第{page}页中含有二级评论,该条回复下面总共含有{count}个二级评论")
                                total_pages = ((count // 20) + 1) if count > 0 else 0
                                for page_pn in range(total_pages):
                                    data_2 = {
                                        # 二级评论的data
                                        'type': type,  # 类型
                                        'oid': oid,  # id
                                        'ps': ps,  # 每页含有条数，不能大于20
                                        'pn': str(page_pn),  # 二级评论页数，需要转换为字符串
                                        'root': rpid  # 一级评论的rpid
                                    }
                                    response = session.get(url_reply, params=data_2, headers=headers, proxies=proxies)
                                    if response.status_code == 200:
                                        json_data = response.json()  # 获得json数据
                                        if 'data' in json_data and 'replies' in json_data['data']:
                                            if not json_data['data']['replies']:  # 检查replies是否为空，如果为空，跳过这一页
                                                print(f"该页replies为空，没有评论")
                                                continue
                                            for comment in json_data['data']['replies']:
                                                name = comment['member']['uname']
                                                sex = comment['member']['sex']
                                                ctime = comment['ctime']
                                                dt_object = datetime.datetime.fromtimestamp(ctime,datetime.timezone.utc)
                                                formatted_time = dt_object.strftime(
                                                    '%Y-%m-%d %H:%M:%S') + ' 北京时间'  # 可以加上时区信息，但通常不需要
                                                like = comment['like']
                                                message = comment['content']['message'].replace('\n', ',')
                                                # 检查是否存在 location 字段
                                                location = comment['reply_control'].get('location','未知')  # 如果不存在，使用 '未知'
                                                location = location.replace('IP属地：', '') if location else location
                                                all_2_comments.append([name, sex, formatted_time, like, message, location, count, rpid])
                                                #all_comments.append([name, sex, formatted_time, like, message, location, count])

                                        else:
                                            print(
                                                f"在第{page_pn + 1}页的JSON响应中缺少 'data' 或 'replies' 键。跳过此页。")
                                    else:
                                        print(f"获取第{page_pn + 1}页失败。状态码: {response.status_code}")
                                random_number = random.uniform(0.2, 0.3)
                                time.sleep(random_number)
                        print(f"已经爬取第{page}页. 状态码: {response.status_code} 即为成功")
                    else:
                        print(f"在页面 {page} 的JSON响应中缺少 'data' 或 'replies' 键。跳过此页。")
                else:
                    print(f"获取页面 {page} 失败。状态码: {response.status_code} 即为失败，请分析原因并尝试重试")
                    # 这里可以处理错误的响应，例如重试或记录错误
                    # 每爬一次就输进去一次，防止爬虫被杀的代码，没法用
                # with open('blue_archive.csv', mode='a', newline='', encoding='utf-8-sig') as file:
                # writer = csv.writer(file)
                # writer.writerows(one_comments)
                random_number = random.uniform(0.5, 0.6)
                print(random_number)
                # 向服务器发出请求后设置延时，以避免请求过于频繁，
                # 不设置也行，用的随机和代理
                # 代价是会给你杀ip
                # 适用范围，1w-3w数据
                time.sleep(random_number)
                break
            except requests.exceptions.RequestException as e:
                print(f"连接失败: {e}")
                if retry < MAX_RETRIES - 1:
                    print(f"正在重试（剩余尝试次数：{MAX_RETRIES - retry - 1}）...")
                    time.sleep(RETRY_INTERVAL)  # 等待一段时间后重试
                else:
                    raise  # 如果达到最大重试次数，则抛出原始异常

        # 将所有评论数据写入CSV文件
with open('2_test.csv', mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地', '二级评论条数'])
    # 写入所有评论数据
    writer.writerows(all_comments)
with open('2_2_test.csv', mode='a', newline='', encoding='utf-8-sig') as file:  # 二级评论条数
    writer = csv.writer(file)
    writer.writerow(['昵称', '性别', '时间', '点赞', '评论', 'IP属地','二级评论条数,条数相同说明在同一个人下面','根id'])
    writer.writerows(all_2_comments)
