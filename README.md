# Reptile 基于bilibili懒加载api爬取b站动态，视频等评论区
# 本项目暂停更新，请移步新的仓库https://github.com/linyuye/Bilibili_crawler

基于bilibili懒加载api爬取b站动态，视频等评论区。
动态评论，视频评论均能爬取。
必须进行去重，爬取评论有重复的。
制作的比较简陋，希望大家提提意见。
失效时间未知！

## QuickStart
# 使用方法
首先将 `.env.example` 重命名为 `.env` 文件，否则无法读取参数

然后打开 `.env` 配置参数即可。核心参数如下：
1. BVID: B站视频的BV号，获取方法在 README 下放可见（需要带有BVxxxxxx，一共12位，库安装 pip3 install bilibili-api-python ）
2（可选）. TUNNEL：代理地址。此处需要你自己找代理地址。（默认不使用）
3（可选）. USER_NAME、PASSWORD：如果开启代理，此处需要填写你自己的账号密码。如果不开启代理，则不需要填（默认不使用，或者参考代理ip网站规则）
4. PS: 爬虫爬取评论区的页数，默认20（不能大于20）
5. DOWN + UP：DOWN是开始爬取的页数，UP是结束爬取的页数
   1. DOWN=1, UP=20: 从第1页开始爬取到第20页

配置完成后。如果是第一次执行，首先得打开终端，执行 `pip install -r requirements.txt` 命令安装依赖

等一切配置完成后，执行 `python 基于懒加载api实现的无限爬取bilibili评论区.py` 命令。即可开始爬取数据


如果想要爬取更多数据，则更新 `.env` 中 DOWN 和 UP 即可。
- 第一次 DOWN=1 UP=20。则第二次 DOWN=21 UP=40
- 不建议一次性爬取过多数据，有概率会被B站封禁。最好一点一点地爬取。

### 关于 BV 号的说明

在 [基于懒加载api实现的无限爬取bilibili评论区.py](基于懒加载api实现的无限爬取bilibili评论区.py) 中，需要找到 bvid 这个参数，填入 BV 号。

BV 号在 B站 视频链接处就可以获取：
- 举个栗子：https://www.bilibili.com/video/BV1v14y1z7MV/?spm_id_from=333.337.search-card.all.click&vd_source=8520816864b1bef4ba13ba9c706bce41
- BV号就是 video/ 后面跟着的一组大小写+数字的参数。
- 复制 BV 号，填入 bvid 即可
- 如果你希望爬取动态，需要在network中寻找相关的oid，可以查看csdn等网站相关教程，若有疑惑可以提issue询问
