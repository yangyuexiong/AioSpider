# AioSpider
#### 基于asyncio与aiohttpp的异步爬虫
#### 百度贴吧异步爬虫

``` 
├── BaiduTeiba
│   ├── AioBaiduSpider.py   ------>异步爬虫
│   └── PlainBaiduSpider.py ------>普通爬虫
```

普通爬虫用于耗时上对比性能的区别

经过对比爬取3页中所有帖子耗时如下:


异步爬虫:06.76秒

普通爬虫:42.63秒

异步是普通的7倍效率