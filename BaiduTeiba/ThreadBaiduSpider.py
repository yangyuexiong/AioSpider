# -*- coding: utf-8 -*-
# @Time    : 2019-08-06 17:58
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ThreadBaiduSpider.py
# @Software: PyCharm


import threading, queue, time, requests, re
from lxml import html

etree = html.etree
first_url = 'https://tieba.baidu.com'
urlQueue = queue.Queue()


def main(kw, page):
    urls = ['https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, i) for i in range(0, page * 50, 50)]
    for i in urls:
        html = requests.get(i)
        h = etree.HTML(html.text)
        list_title = h.xpath('//*[@id="thread_list"]/li/div/div//a/@href')
        q_list = [urlQueue.put(first_url + i) for i in list(filter(lambda x: re.findall(r'^/p/\d+', x), list_title))]
    print(urlQueue.qsize())


def save_data(d):
    with open('thread_post.json', 'a') as f:
        f.write(str(d))


def fetchUrl(urlQueue):
    while True:
        try:
            # 不阻塞的读取队列数据
            url = urlQueue.get_nowait()
            i = urlQueue.qsize()
        except Exception as e:
            break
        # print('线程名称 %s, Url: %s ' % (threading.currentThread().name, url))
        # print('线程名称id %s' % (threading.get_ident()))
        try:
            html2 = requests.get(url)
            h = etree.HTML(html2.text)
            title = h.xpath('//*[@id="j_core_title_wrap"]/h3/text()')
            auth = h.xpath('//*[@id="j_p_postlist"]/div[1]/div[1]/ul/li[3]/a/text()')
            content = h.xpath("//*[contains(@id,'post_content_')]/text()")
            imgs = h.xpath("//*[contains(@id,'post_content_')]/img/@src")

            post = {
                'url': url,
                '标题': title[0],
                '作者': auth[0],
                '内容': content[0],
                '图片': imgs
            }
            new = "{}\n".format(post)
            save_data(new)
        except Exception as e:
            continue


if __name__ == '__main__':
    pass
    main('地下城与勇士', 5)
    startTime = time.time()
    threads = []
    for i in range(0, urlQueue.qsize()):
        t = threading.Thread(target=fetchUrl, args=(urlQueue,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
        t.join()
    endTime = time.time()
    print('总耗时: %s ' % (endTime - startTime))
