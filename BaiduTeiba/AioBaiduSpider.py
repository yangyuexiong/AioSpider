# -*- coding: utf-8 -*-
# @Time    : 2019-08-02 16:41
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : AioBaiduSpider.py
# @Software: PyCharm


import asyncio
import aiohttp
from lxml import html
import datetime
import re
import threading

etree = html.etree

first_url = 'https://tieba.baidu.com'

q = asyncio.Queue()


async def get_url(url, header=None):
    """请求url"""
    # print('get_url thread_id', threading.get_ident())

    sem = asyncio.Semaphore(100)  # 并发数量限制
    # timeout = aiohttp.ClientTimeout(total=3)  # 超时
    async with sem:
        async with aiohttp.ClientSession(headers=header, cookies='') as session:
            async with session.get(url) as resp:
                if resp.status in [200, 201]:
                    data = await resp.text()
                    # print(data)
                    return data


async def parse(url):
    """解析每页的每篇帖子的url放入队列"""
    # print('parse thread_id', threading.get_ident())

    html = await get_url(url)
    h = etree.HTML(html)
    list_title = h.xpath('//*[@id="thread_list"]/li/div/div//a/@href')
    new_list = list(filter(lambda x: re.findall(r'^/p/\d+', x), list_title))
    # print(new_list)
    for i in new_list:
        main_url = first_url + i
        # print(main_url)
        await q.put(main_url)

    print('队列长度:{}'.format(q.qsize()))
    return


async def parse2():
    """从队列中取出每篇帖子解析出 标题,内容,作者等..."""
    # print('parse2 thread_id', threading.get_ident())

    if q.qsize() != 0:
        url = await q.get()
        html = await get_url(url)
        h = etree.HTML(html)
        title = h.xpath('//*[@id="j_core_title_wrap"]/h3/text()')
        auth = h.xpath('//*[@id="j_p_postlist"]/div[1]/div[1]/ul/li[3]/a/text()')
        content = h.xpath("//*[contains(@id,'post_content_')]/text()")
        imgs = h.xpath("//*[contains(@id,'post_content_')]/img/@src")

        # print(title)
        # print(auth)
        # print(content[0])

        post = {
            'url': url,
            '标题': title[0],
            '作者': auth[0],
            '内容': content[0],
            '图片': imgs
        }
        new = "{}\n".format(post)
        return new
    else:
        print('队列已经为空了！')


async def save_data():
    """保存"""
    p = await parse2()
    with open('aio_post.json', 'a') as f:
        f.write(str(p))


async def main(kw, page):
    """
    main

    kw:贴把名称
    page:需要爬取的页数数量

    """
    # print('main thread_id', threading.get_ident())

    start_time = datetime.datetime.now()
    print(start_time)
    print('===任务1:获取每个父页面===')

    """优化前"""
    # urls = ['https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, i) for i in range(0, page * 50, 50)]
    # print(urls)
    # tasks = [asyncio.create_task(parse(url)) for url in urls]

    """优化后"""
    urls = [q.put_nowait('https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, i)) for i in
            range(0, page * 50, 50)]
    tasks = [asyncio.create_task(parse(q.get_nowait())) for url in range(0, q.qsize())]
    await asyncio.wait(tasks)
    print('完成\n')
    # one_time = datetime.datetime.now() - start_time
    # print('第一个总耗时{}'.format(one_time))

    print('===任务2:子页面每篇帖子爬取===')
    print('队列长度:{}'.format(q.qsize()))
    tasks2 = [asyncio.create_task(save_data()) for _ in range(0, q.qsize() - 1)]
    await asyncio.wait(tasks2)
    print('完成\n')
    all_time = datetime.datetime.now() - start_time
    print('总耗时:{}'.format(all_time))


if __name__ == '__main__':
    pass
    asyncio.run(main('地下城与勇士', 5))
