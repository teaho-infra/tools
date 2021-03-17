# -*- coding: utf-8 -*-
import json
import os
from functools import reduce
from urllib import parse

import execjs
import requests

# 我的本地代理
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890'
}


def get_sign(data):
    with open('./get_sign.js', 'r', encoding='utf-8') as f:
        text = f.read()

    js_data = execjs.compile(text)
    sign = js_data.call('get_sign', data)
    return sign


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'Referer': 'https://y.qq.com/portal/singer_list.html',
    # 参考链接 https://y.qq.com/portal/singer_list.html#page=1&index=1&
}


def join_str(x, y):
    return x.name + y.name


def get_music(p=1, n=5, w=None):
    """
        p:页数，从1开始
        n:每一页显示的条数
        w:搜索关键字
    """
    # 音乐搜索url
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p={}&n={}&w={}'.format(p, n, w)
    response = requests.get(url, proxies=proxies)
    datas = response.text[9: len(response.text.strip()) - 1]
    # 返回songmid
    songmid = json.loads(datas)['data']['song']['list'][0]['songmid']
    song_name = json.loads(datas)['data']['song']['list'][0]['songname']
    singers = json.loads(datas)['data']['song']['list'][0]['singer']
    singer_name = reduce(lambda x, y: x + '&' + y, map(lambda x: x['name'], singers))
    print('songmid:{}, song_name:{}, singer_name:{}'.format(songmid, song_name, singer_name))

    # # 在浏览器中播放
    # # browser = webdriver.Chrome()
    # # browser.get(show_music)
    #
    # # 本地生成音频文件
    # response = requests.get(show_music)
    # with open(songmid+'.m4a', 'wb')as f:
    #     f.write(response.content)
    #     f.close()

    download(songmid, song_name, singer_name)

    return


def download(song_mid, song_name, singer_name):
    qq_number = '479255131'  # 请修改你的QQ号
    data = '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch"' \
           ',"param":{"guid":"4803422090","calltype":0,"userip":""}},' \
           '"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey",' \
           '"param":{"guid":"4803422090","songmid":["%s"],"songtype":[0],' \
           '"uin":"%s","loginflag":1,"platform":"20"}},"comm":{"uin":%s,"format":"json","ct":24,"cv":0}}' % (
               str(song_mid), str(qq_number), str(qq_number))

    sign = get_sign(data)
    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getplaysongvkey27494207511290925' \
          '&g_tk=1291538537&sign={}&loginUin={}' \
          '&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0' \
          '&platform=yqq.json&needNewCode=0&data={}'.format(sign, qq_number, parse.quote(data))

    html = requests.get(url, headers=headers, proxies=proxies).json()

    try:
        purl = html['req_0']['data']['midurlinfo'][0]['purl']

        url = 'https://113.105.167.153/amobile.music.tc.qq.com/{}'.format(purl)

        html = requests.get(url, headers=headers, verify=False, proxies=proxies)

        html.encoding = 'utf-8'

        sing_file_name = '{} - {}'.format(singer_name, song_name)

        filename = './song'

        if html.status_code != 403:
            if not os.path.exists(filename):
                os.makedirs(filename)

            with open('./song/{}.m4a'.format(sing_file_name), 'wb') as f:
                print('\n正在下载{}歌曲.....\n'.format(sing_file_name))
                f.write(html.content)

            print('finish')
    except:
        print('查询权限失败，或没有查到对应的歌曲')


def main():
    name = get_music(w='don look back in anger')


if __name__ == '__main__':
    main()
