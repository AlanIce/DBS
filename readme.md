DBS开发文档
==========

## 项目介绍
DBS(Douban Spider)
豆瓣爬虫项目

## Fetcher
Fetcher主要作用是填充URLQueue

 * 一级队列都是标签列表
 * 二级队列是20部电影的页面
 * 三级队列是电影的详情页面

## Parser
Fetcher主要作用是从URLQueue取出URL，并对URL的内容进行解析，构造出Model并填充到ModelQueue中去

## Saver
Saver的主要作用是从ModelQueue中取出Model，并对Model进行持久化操作。

## 数据库的表结构
|字段名			|注释
|---------------|------
|id 			|ID
|title 			|电影
|directors		|导演
|writers		|编剧
|casts			|主演
|genres			|类型
|countries		|制片国家/地区
|languages		|语言
|pubdates		|上映日期
|durations		|片长
|aka			|又名
|summary		|简介
|rating			|评分
|rating_count	|评分人数
|image_url		|海报链接
