import json
import os
import random
import requests
import sys
import subprocess
import yt_dlp

from .Controller.bililive import BiliLiveApi

class Streamer:
    def get_stream(live_link):
        ydl_opts = {
            'proxy': proxy
        }
        play_info = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(live_link, download=False)
            for f in info["formats"]:
                play_info[f['format_id']] = f['url']
                print(f"{f['format_id']}: {f['resolution']} - {f['fps']}FPS")
            id = input('输入目标序号：\n')
            if id:
                return play_info[id]
            return info['url']

    def ffmpeg_re_stream(raw_url, http_proxy, rtmp_code):
        rtmp_server = "rtmp://{}/live-bvc/{}".format(random.choice(ip_list), rtmp_code)
        headers = ['-headers', ''.join('%s: %s\r\n' % x for x in fake_headers.items())]
        args = ['ffmpeg', '-re', '-y', *headers, '-http_proxy', http_proxy,
                '-i', raw_url,
                '-c', 'copy', '-f', 'flv',
                rtmp_server]
        try:
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with proc.stdout as stdout, open('ffmpeg.log', 'w+') as logfile:
                for line in iter(stdout.readline, b''):
                    decode_line = line.decode(errors='ignore')
                    logfile.write(decode_line)
            retval = proc.wait()
        except KeyboardInterrupt:
            if sys.platform != 'win32':
                proc.communicate(b'q')
            raise
        return retval


def before_first_run(cookie_file_path):
    if  __it_txy():
        ip_list = __dns_query("txy.live-push.bilivideo.com", "sys")
    else:
        ip_list = __dns_query("live-push.bilivideo.com")
    return ip_list, BiliLiveApi(__load_cookies(cookie_file_path))

def __it_txy() -> bool:
    with requests.Session() as s:
        try:
            txy_region_in_asia = s.get('http://metadata.tencentyun.com/latest/meta-data/placement/region').text.startswith('ap')
            return txy_region_in_asia
        except Exception:
            pass
    return False

def __dns_query(hostname: str, type: str = "http") -> list:
    httpdns_url = "http://182.254.116.116/d"
    parmas = {
        'dn': hostname,
        'ttl': 1,
    }
    if type in "http":
        with requests.Session() as s:
            ip_text = s.get(httpdns_url, params=parmas, timeout=3).text
            return ip_text.split(',')[0].split(';')
    import socket
    return list(map(lambda x: x[4][0], socket.getaddrinfo(f'{hostname}.', 1935, type=socket.SOCK_STREAM)))

def __load_cookies(cookie_file = 'cookies.json') -> dict:
    cookies = {}
    with open(cookie_file, encoding='utf-8') as stream:
        s = json.load(stream)
        for i in s["cookie_info"]["cookies"]:
            cookies[i["name"]] = i["value"]
        cookies["access_token"] = s["token_info"]["access_token"]
    return cookies

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

ip_list, bililive_controller = before_first_run()

if __name__ == '__main__':

    proxy = "http://172.31.64.1:7890"
    link = input('输入频道地址：\n')
    link = "https://www.youtube.com/channel/UCf-PcSHzYAtfcoiBr5C9DZA"
    if "/playlist" in link:
        pass
    if "/channel" in link or "/@" in link:
        link+="/live"
    if link.endswith("/live") or "/watch?" in link:
        raw_url = get_stream(link)
    ffmpeg_re_stream(raw_url, proxy)
