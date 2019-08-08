# -*- coding: utf-8 -*-
# @Time    : 2019-08-06 10:35
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : PlainBaiduSpider.py
# @Software: PyCharm


import requests
from lxml import html
import datetime
import re

etree = html.etree
first_url = 'https://tieba.baidu.com'


def save_data(d):
    with open('plain_post.json', 'a') as f:
        f.write(str(d))


def main(kw, page):
    """main"""
    start_time = datetime.datetime.now()
    print(start_time)
    urls = ['https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, i) for i in range(0, page * 50, 50)]
    for i in urls:
        new_list = []
        html = requests.get(i)
        h = etree.HTML(html.text)
        list_title = h.xpath('//*[@id="thread_list"]/li/div/div//a/@href')
        new_list = list(filter(lambda x: re.findall(r'^/p/\d+', x), list_title))
        print(len(new_list))

    for j in new_list:
        main_url = first_url + j
        html2 = requests.get(main_url)

        h = etree.HTML(html2.text)
        title = h.xpath('//*[@id="j_core_title_wrap"]/h3/text()')
        auth = h.xpath('//*[@id="j_p_postlist"]/div[1]/div[1]/ul/li[3]/a/text()')
        content = h.xpath("//*[contains(@id,'post_content_')]/text()")
        imgs = h.xpath("//*[contains(@id,'post_content_')]/img/@src")

        post = {
            'url': main_url,
            '标题': title[0],
            '作者': auth[0],
            '内容': content[0],
            '图片': imgs
        }
        new = "{}\n".format(post)
        save_data(new)

    all_time = datetime.datetime.now() - start_time
    print('总耗时:{}'.format(all_time))


if __name__ == '__main__':
    main('地下城与勇士', 5)
