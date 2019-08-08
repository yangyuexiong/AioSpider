# AioSpider
#### 基于asyncio与aiohttpp的异步爬虫
#### 百度贴吧异步爬虫

``` 
├── BaiduTeiba
│   ├── AioBaiduSpider.py    ------>异步爬虫
│   ├── PlainBaiduSpider.py  ------>普通爬虫
│   ├── ThreadBaiduSpider.py ------>多线程爬虫
│   ├── aio_post.json
│   ├── plain_post.json
│   └── thread_post.json
└── README.md
```

普通爬虫用于耗时上对比性能的区别

经过对比爬取3页中所有帖子耗时如下:


异步爬虫: 5.66～6.76秒

多线程爬虫: 4.27～6.59秒

普通爬虫: 39.95～43.10秒

异步与多线程爬虫是普通的约8倍效率