import requests
import random
import time
from fake_useragent import UserAgent

# 定义关键词和标签
keywords = {
    "keyword_cj": ["互动抽奖"],
    "keyword_cj_yuan": ["互动抽奖 #原神#"],
    "keyword_yuan": ["原神"],
    "keyword_zhou": ["明日方舟"],
    "keyword_nong": ["王者荣耀"],
    "keyword_beng": ["崩坏"],
    "keyword_qiong": ["星穹铁道"],
    "keyword_xian": ["全自动", "模块", "仙驱", "先驱"],
    "keyword_yuanpi": ["猴"]
}

tags = {
    "tag_nor": "【 普通丨待定 】",
    "tag_cj": "【 动态抽奖 】",
    "tag_cj_yuan": "【 原神动态抽奖 】",
    "tag_yuan": "【 稀有丨我超，原！】",
    "tag_zhou": "【 稀有丨我超，舟！】",
    "tag_nong": "【 稀有丨我超，农！】",
    "tag_qiong": "【 稀有丨我超，穹！】",
    "tag_yuanzhou": "【 史诗丨原 & 粥！】",
    "tag_yuannong": "【 史诗丨原 & 农！】",
    "tag_nongzhou": "【 史诗丨农 & 舟！】",
    "tag_yuanqiong": "【 神话丨原 & 穹！】",
    "tag_yuanbeng": "【 神话丨原 & 崩！】",
    "tag_xian": "【 仙器丨达摩克利斯之剑 】",
    "tag_sanxiang": "【 传奇丨三相之力 】",
    "tag_misan": "【 传奇丨三位一体 】",
    "tag_yuanpi": "【 结晶丨原批 】",
    "tag_mxz_1": "【 米学长丨认识Mihoyo 】",
    "tag_mxz_2": "【 米学长丨腾讯打压 】",
    "tag_mxz_3": "【 米学长丨黑暗降临 】",
    "tag_mxz_4": "【 米学长丨国产之光 】",
    "tag_mxz_5": "【 米学长丨Mihoyo是天 】"
}

def get_user_all_dynamic(uid, proxies=None):
    offset = ""
    items = []

    while True:
        data = get_user_dynamic(uid, offset)
        random_delay()
        # print(data)
        if not data or "data" not in data:
            return items

        items += data["data"]["items"]
        has_more = data["data"]["has_more"]
        if has_more:
            offset = data["data"]["offset"]
        else:
            break

    print(len(items))
    return items


# 获取用户动态数据, 从 offset = 0 开始
def get_user_dynamic(uid, offset="", proxies=None):
    url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={offset}&host_mid={uid}&timezone_offset=420&platform=web&features=itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote&web_location=333.999'
    cookie = "your_cookie_here"

    headers = {
        'authority': 'api.bilibili.com',
        'method': 'GET',
        'path': f'/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={uid}&timezone_offset=420&platform=web&features=itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote&web_location=333.999',
        'scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Origin': 'https://space.bilibili.com',
        'Priority': 'u=1, i',
        'Referer': f'https://space.bilibili.com/{uid}/dynamic',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': UserAgent().random
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed: {response.status_code} {response.text}")
        return None

# 判断是否包含关键词
def has_keyword(content, keywords):
    return any(keyword in content for keyword in keywords)

# 计算关键词出现次数
def get_keyword_count(content, keywords):
    count = 0
    for keyword in keywords:
        count += content.count(keyword)
    return count

# 分析用户动态数据并返回标签
def analyze_user(uid, proxies=None):
    data = get_user_all_dynamic(uid, proxies)
    if not data:
        return "用户数据获取失败"

    content = str(data)
    tag_results = []

    # 原神相关
    if has_keyword(content, keywords["keyword_yuan"]):
        if has_keyword(content, keywords["keyword_yuanpi"]):
            tag_results.append(tags["tag_yuanpi"])
        if has_keyword(content, keywords["keyword_xian"]):
            tag_results.append(tags["tag_xian"])
        if has_keyword(content, keywords["keyword_beng"]) and has_keyword(content, keywords["keyword_qiong"]):
            tag_results.append(tags["tag_misan"])
        elif has_keyword(content, keywords["keyword_nong"]) and has_keyword(content, keywords["keyword_zhou"]):
            tag_results.append(tags["tag_sanxiang"])
        elif has_keyword(content, keywords["keyword_qiong"]):
            tag_results.append(tags["tag_yuanqiong"])
        elif has_keyword(content, keywords["keyword_beng"]):
            tag_results.append(tags["tag_yuanbeng"])
        elif has_keyword(content, keywords["keyword_zhou"]):
            tag_results.append(tags["tag_yuanzhou"])
        elif has_keyword(content, keywords["keyword_nong"]):
            tag_results.append(tags["tag_yuannong"])
        else:
            tag_results.append(tags["tag_yuan"])
        count = get_keyword_count(content, keywords["keyword_yuan"])
        if count >= 0 and count <= 5:
            tag_results.append(tags["tag_mxz_1"])
        elif count > 5 and count <= 10:
            tag_results.append(tags["tag_mxz_2"])
        elif count > 10 and count <= 20:
            tag_results.append(tags["tag_mxz_3"])
        elif count > 20 and count <= 30:
            tag_results.append(tags["tag_mxz_4"])
        else:
            tag_results.append(tags["tag_mxz_5"])
        if has_keyword(content, keywords["keyword_cj_yuan"]):
            tag_results.append(tags["tag_cj_yuan"])
        return " ".join(tag_results)

    # 王者荣耀相关
    if has_keyword(content, keywords["keyword_nong"]):
        if has_keyword(content, keywords["keyword_zhou"]):
            return tags["tag_nongzhou"]
        else:
            return tags["tag_nong"]

    # 明日方舟相关
    if has_keyword(content, keywords["keyword_zhou"]):
        return tags["tag_zhou"]

    # 抽奖标签
    if has_keyword(content, keywords["keyword_cj"]):
        return tags["tag_cj"]

    return tags["tag_nor"]

# 随机延迟函数
def random_delay(min_delay=2, max_delay=10):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

# 用户列表
user_list = [
    21587347,  # 米学长国产之光, 爬全部数据后：【 仙器丨达摩克利斯之剑 】 【 传奇丨三位一体 】 【 米学长丨Mihoyo是天 】 【 原神动态抽奖 】
    385075616,  # 【 稀有丨我超，原！】【 米学长丨黑暗降临 】【 原神动态抽奖 】，爬全部数据后：【 稀有丨我超，原！】 【 米学长丨Mihoyo是天 】 【 原神动态抽奖 】
    430277305,  # 【 传奇丨三位一体 】【 米学长丨国产之光 】【 原神动态抽奖 】, 爬全部数据后：【 传奇丨三位一体 】 【 米学长丨Mihoyo是天 】 【 原神动态抽奖 】
    351027337, #  【 传奇丨三位一体 】【 米学长丨腾讯打压 】，爬全部数据后：【 仙器丨达摩克利斯之剑 】 【 传奇丨三位一体 】 【 米学长丨Mihoyo是天 】 【 原神动态抽奖 】
]

if __name__ == "__main__":
    # 设置代理（如果需要）
    # proxies = {
    #     'http': 'http://your_proxy_here',
    #     'https': 'http://your_proxy_here'
    # }

    for uid in user_list:
        print(f"uid = {uid}, result = {analyze_user(uid)}")
