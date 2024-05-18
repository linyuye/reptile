# Reptile 基于bilibili懒加载api爬取b站动态，视频等评论区

基于bilibili懒加载api爬取b站动态，视频等评论区。
动态评论，视频评论均能爬取。
必须进行去重，爬取评论有重复的。
制作的比较简陋，希望大家提提意见。
失效时间未知！

## QuickStart

0. 配置参数

打开你想要运行的脚本文件，阅读注释，填写必要的参数。

1. 启动命令行

2. 安装必要依赖
```
pip install -r requirments.txt
```



3. 执行脚本
```
python <脚本名词>.py
```

### 关于 BV 号的说明

在 [基于懒加载api实现的无限爬取bilibili评论区.py](基于懒加载api实现的无限爬取bilibili评论区.py) 中，需要找到 bvid 这个参数，填入 BV 号。

BV 号在 B站 视频链接处就可以获取：
- 举个栗子：https://www.bilibili.com/video/BV1v14y1z7MV/?spm_id_from=333.337.search-card.all.click&vd_source=8520816864b1bef4ba13ba9c706bce41
- BV号就是 video/ 后面跟着的一组大小写+数字的参数。
- 复制 BV 号，填入 bvid 即可


## TODO

脚本很多参数都是硬编码在程序之中的，希望后续可以在运行期间自行输入，方便小白使用