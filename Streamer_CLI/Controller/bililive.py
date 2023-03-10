import requests

class BiliLiveApi:
    def __init__(self, cookies) -> None:
        # GET
        self.live_info_url = "https://api.live.bilibili.com/xlive/web-ucenter/user/live_info"
        self.room_area_switch_url = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch"
        # POST
        self.start_live_url = "https://api.live.bilibili.com/room/v1/Room/startLive"
        self.stop_live_url = "https://api.live.bilibili.com/room/v1/Room/stopLive"
        self.room_update_url = "https://api.live.bilibili.com/room/v1/Room/update"
        self.postdata = {
            'csrf_token': cookies['bili_jct'],
            'csrf': cookies['bili_jct'],
        }
        # Users setting
        self.s = requests.Session()
        self.s.cookies = cookies
        self.s.headers = fake_headers
        self.s.headers['Origin'] = "https://link.bilibili.com"
        self.s.headers['Referer'] = "https://link.bilibili.com/p/center/index"
        self.rtmp_code = ""

    def refresh_room_id(self) -> int:
        """
        获取用户直播间号

        Returns:
            code: API返回码
        """
        info = self.s.get(self.live_info_url, timeout=3).json()
        self.postdata['room_id'] = info['data']['room_id']
        return info['code']

    def room_area_switch(self, platform: str = "pc", area_parent_id: int = 10, area_id: int = 33) -> int:
        """
        修改直播间分区

        Args:
            platform (str): 开播平台
            area_parent_id (int): 直播父分区id
            area_id (int): 直播子分区id

        Returns:
            code: API返回码
        """
        data = {
            'platform': platform,
            'area_parent_id': area_parent_id,
            'area_id': area_id,
        }
        code = self.s.get(self.room_update_url, data=data, timeout=3).json()['code']
        return code

    def room_update(self, title: str) -> int:
        """
        修改直播间标题

        Args:
            title (str): 直播间标题

        Returns:
            code: API返回码
        """
        data = self.postdata.copy()
        data['title'] = title
        code = self.s.post(self.room_update_url, data=data, timeout=3).json()['code']
        return code

    def start_live(self, platform: str, area_id: int) -> str:
        """
        上播

        Args:
            platform (str): 开播平台
            area_id (int): 直播子分区id

        Returns:
            code: API返回码
        """
        data = self.postdata.copy()
        data['area_v2'] = area_id
        data['platform'] = platform
        info = self.s.post(self.start_live_url, data=data, timeout=3).json()
        if info['code'] == 0:
            self.rtmp_code = info['data']['rtmp']['code']
        return info['code']

    def stop_live(self, platform: str) -> str:
        """
        下播

        Args:
            platform (str): 开播平台

        Returns:
            code: API返回码
        """
        data = self.postdata.copy()
        data['platform'] = platform
        code = self.s.post(self.stop_live_url, data=data, timeout=3).json()['code']
        return code