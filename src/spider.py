# coding:utf-8
import requests
from flask import json
from requests.exceptions import RequestException
import re

def get_response(url):
    '''
    抓取HTML页面
    :param url:
    :return:
    '''
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        referer = 'http://www.baidu.com'
        headers = {"User-Agent": user_agent, 'Referer': referer}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    '''
    通过正则表达式解析html，并格式化数据
    :param html:
    :return:
    '''

    pat = re.compile(
        '<dd>.*?board-index.*?">(.*?)</i>.*?"name"><a.*?">(.*?)</a>.*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)

    # 正则表达式找到所有匹配的内容
    items = re.findall(pat, html)

    #格式化数据
    for item in items:
        yield {
            '排名': item[0],
            '影片名称': item[1],
            '演员': item[2].strip()[2:],
            '上映时间': item[3].strip()[5:],
            '评分': item[4] + item[5]
        }

def write_into_file(conrent):
    '''
    将抓取的内容写入文件
    :param conrent:
    :return:
    '''
    with open('result.txt', 'a',encoding='utf-8') as f:
        f.write(json.dumps(conrent, ensure_ascii=False) + '\n')
        f.close()

def get_and_save_one_page(offset):
    '''
    读取并保存第offset页的数据
    :param offset:
    :return:
    '''
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_response(url)
    for item in parse_one_page(html):
        write_into_file(item)

if __name__ == '__main__':

    for i in range(10):
        offset = 10*i
        get_and_save_one_page(offset)