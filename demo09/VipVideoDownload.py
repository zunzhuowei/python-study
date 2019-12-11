import os
import re
from urllib import request

import requests


class VipVideoDownload:

    def __init__(self, name='_'):
        ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        self.__headers = {
            'User-Agent': ua,
        }
        self.__s = requests.Session()
        self.__s.headers = self.__headers
        self.__api = 'http://jx.api.163ren.com/api.php'
        self.name = name

    def __cbk(self, a, b, c):
        per = 100 * a * b / c
        if per > 100:
            per = 100
        print('已下载: {:.2f}%'.format(per))

    def __get_api_arg(self, video_url):
        url = 'http://jx.api.163ren.com/vod.php?url={}'.format(video_url)
        r = self.__s.get(url)
        if r.status_code == 200:
            return re.compile('url.*?\'(.*?)\'').findall(r.text)[0]

    def __get_real_url(self, video_url):
        data = {
            'url': self.__get_api_arg(video_url),
            'up': 0,
        }
        r = self.__s.post(self.__api, data=data)
        if r.status_code == 200:
            js_data = r.json()
            if js_data['msg'] == 'ok':
                real_url = js_data['url']
                ext = js_data['ext']
                return real_url, ext
            else:
                print(js_data['msg'])
                exit(0)

    def download(self, video_url):
        real_url, ext = self.__get_real_url(video_url)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '{}.{}'.format(self.name, ext))
        request.urlretrieve(real_url, filename, reporthook=self.__cbk)


if __name__ == '__main__':
    vv = VipVideoDownload()
    vv.name = '心理罪'
    v_url = 'https://v.qq.com/x/cover/cqqoh6bdcwn0oyu.html'
    vv.download(v_url)