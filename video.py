import requests
import json
import os
import time
import utils

def rough_number(num:int, idigits=1):
    """
    This function can round off one number.
    """
    if num >= 100000000:
        num = round(num/100000000, idigits)
        return f"{num:.{idigits}f}亿"
    elif num >= 10000:
        num = round(num/10000, idigits)
        return f"{num:.{idigits}f}万"
    else:
        return num

class videoInfo():
    def __init__(self, aid: int, bvid: str):
        infoUrl = "https://api.bilibili.com/x/web-interface/view"
        params = {
          "aid": aid,
          "bvid": bvid
        }
        self.bvid = bvid
        response_info = requests.get(url=infoUrl, params=params,headers=utils.load_headers(), cookies=utils.load_cookie())
        if response_info.status_code == requests.codes.OK:
            self.information:dict = json.loads(response_info.text)
            with open(f"Bilibili_scrape/data/{bvid}_info.json", 'w') as f:
                f.write(json.dumps(self.information, indent="\t", ensure_ascii=False))
        else:
            print(f"The request to get video detailed information is wrong. The response status code is {response_info.status_code}.")
        self.load_video_info()

    def load_video_info(self):
        with open(f"Bilibili_scrape/data/{self.bvid}_info.json", 'r') as f:
            self.info:dict = json.loads(f.read())

    def title(self):
        t = self.info['data']['title']
        try:
            os.mkdir(t)
        except FileExistsError:
            pass

        return t
    
    def url(self):
        string = "www.bilibili.com/" + self.info['data']['bvid'] + "/"

        return string
    
    def bvid(self):
        return self.info['data']['bvid']
    
    def aid(self):
        return self.info['data']['aid']
    
    def upload_date(self):
        ctime = self.info['data']['pubdate']
        upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))

        return upload_date
    
    def play_number(self, rough:bool=True):
        """
        Params
        ----------
        rough: Default True, this method rounds off the play number. If False, this method returns detailed number.
            eg: 380.0万、1.2亿
        """
        play_number: int|float = self.info['data']['stat']['view']
        if rough:
            return rough_number(play_number)
        else:
            return play_number
        
    def like_number(self, rough:bool=True):
        """
        Params
        ----------
        rough: Default True, this method rounds off the play number. If False, this method returns detailed number.
            eg: 380.0万、1.2亿
        """
        like_number: int|float = self.info['data']['stat']['like']
        if rough:
            return rough_number(like_number)
        else:
            return like_number
        
    def coin_number(self,rough:bool=True):
        """
        Params
        ----------
        rough: Default True, this method rounds off the play number. If False, this method returns detailed number.
            eg: 380.0万、1.2亿
        """
        coin_number: int|float = self.info['data']['stat']['coin']
        if rough:
            return rough_number(coin_number)
        else:
            return coin_number
        
    def favorite_number(self, rough:bool=True):
        """
        Params
        ----------
        rough: Default True, this method rounds off the play number. If False, this method returns detailed number.
            eg: 380.0万、1.2亿
        """
        favorite_number: int|float = self.info['data']['stat']['favorite']
        if rough:
            return rough_number(favorite_number)
        else:
            return favorite_number
        
    def pic(self):
        pic_url = self.info['data']['pic']
        title = self.title()
        res = requests.get(url=pic_url, headers=utils.load_headers("user-agent"))
        if res.status_code == requests.codes.OK:
            with open(f"{title}/{title}.png", 'wb') as f:
                f.write(res.content)
            print(f"The picture of cover has saved.")
        else:
            print(f"The request is wrong, the request status code is {res.status_code}.")

    def description(self):
        return self.info['data']['desc']
    
    def danmu_number(self, rough:bool=True):
        danmu_number = self.info['data']['stat']['danmuku']
        if rough:
            return rough_number(danmu_number)
        else:
            return danmu_number
        
    def share_number(self, rough:bool=True):
        share_number = self.info['data']['stat']['share']
        if rough:
            return rough_number(share_number)
        else:
            return share_number
        
    def reply_number(self, rough:bool=True):
        reply_number = self.info['data']['stat']['reply']
        if rough:
            return rough_number(reply_number)
        else:
            return reply_number
        
    def owner_name(self):
        return self.info['data']['owner']['name']
    
    def owner_space(self):
        mid = self.info['data']['owner']['mid']
        owner_space_url = "https://space.bilibili.com/" + str(mid)

        return owner_space_url

    def delete_temporary_file(self):
        """
        Delete the temporary file. Such as json.
        """
        os.remove(f"Bilibili_scrape/data/{self.bvid}_info.json")

class videoPlayUrl():
    def __init__(self, aid:int, bvid:str, cid:int, qn:int=125):
        play_url = "https://api.bilibili.com/x/player/wbi/playurl"
        params = {
            "aid": aid,
            "cid": cid,
            "bvid": bvid,
            "qn": qn,
            "otype": "json",
            "fnval": 4048,
            "platform": "web"
        }
        self.bvid = bvid
        response_play = requests.get(url=play_url, params=params, headers=utils.load_headers(), cookies=utils.load_cookie())
        if response_play.status_code == requests.codes.OK:
            self.video_source_urls:dict = json.loads(response_play.text)
            with open(f"Bilibili_scrape/data/{self.bvid}_playUrl.json", "w") as f:
                f.write(json.dumps(self.video_source_urls, indent="\t", ensure_ascii=False))
        else:
            print(f"The request to get video detailed information is wrong. The response status code is {response_play.status_code}.")
        self.load_video_source_urls()

    def load_video_source_urls(self):
        with open(f"Bilibili_scrape/data/{self.bvid}_playUrl.json", 'r') as f:
            self.play:dict = json.loads(f.read())

    def quality(self) -> int:
        accept_description:list = self.play['data']['accept_description']
        accept_quality:list = self.play['data']['accept_quality']
        string_shown2user = ""
        for i in range(len(accept_description)):
            if i == len(accept_description):
                string_shown2user = string_shown2user + str(accept_quality[i]) + ":" +  accept_description[i]
            else:
                string_shown2user = string_shown2user + str(accept_quality[i]) + ":" + accept_description[i] + ";"
        print(string_shown2user)
        return accept_quality[0] # 如果你需要自定义下载视频的清晰度，把这行代码注释掉
        while True:
            quality = int(input(f"请选择输入你想要下载的视频清晰度："))
            if quality in accept_quality:
                break
            else:
                print("没有你想要的清晰度，请重新输入")
                continue
        
        return quality
    
    def video_source_url(self) -> str:
        import sys

        quality = self.quality()
        video_url_list:list = self.play['data']['dash']['video']
        target_dicts = [item for item in video_url_list if item.get("id") == quality]
        for item in target_dicts:
            base_url = item.get('base_url')
            backup_urls = item.get("backup_url", [])
            if base_url:
                try:
                    response = requests.head(url=base_url, headers=utils.load_headers(), cookies=utils.load_cookie())
                    if response.status_code == requests.codes.OK:
                        return base_url
                    else:
                        print(f"The status code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"base_url不可用，错误为:{e}")
            for backuo_url in backup_urls:
                try:
                    response = requests.head(url=backuo_url, headers=utils.load_headers(), cookies=utils.load_cookie())
                    if response.status_code == requests.codes.OK:
                        return backuo_url
                    else:
                        print(f"The response status code from backup_url is {response.status_code}")
                except requests.RequestException as e:
                    print(f"backup_url不可用，错误为：{e}")
        print(f"目前出现不明状况，该清晰度视频无法下载，请稍后重试或选择其他清晰度。")
        sys.exit()

    def audio_source_url(self, quality:int = 30280):
        import sys

        audio_url_list:list = self.play['data']['dash']['audio']
        for item in audio_url_list:
            if item.get("id") == quality:
                base_url = item.get("base_url")
                backup_urls = item.get("backup_url", [])
                if base_url:
                    try:
                        response = requests.head(url=base_url, headers=utils.load_headers(), cookies=utils.load_cookie())
                        if response.status_code == requests.codes.OK:
                            return base_url
                        else:
                            print(f"The response status code from base_url: {response.status_code}")
                    except requests.RequestException as e:
                        print(f"base_urrl不可用，错误为：{e}")
                for backup_url in backup_urls:
                    try:
                        response = requests.head(url=backup_url, headers=utils.load_headers(), cookies=utils.load_cookie())
                        if response.status_code == requests.codes.OK:
                            return backup_url
                        else:
                            print(f"The response status code from backup_url: {response.status_code}")
                    except requests.RequestException as e:
                        print(f"backup_url不可用，错误为{e}")
        print(f"目前出现不明状况，该品质的音频无法下载，请稍后重试或选择其他品质的音频。")
        sys.exit()

    def delete_temporary_file(self, tem_video:bool=False, tem_audio:bool=False,):
        """
        Delete the temporary files.

        Params
        ----------
        tem_video: Default `False`. If `True`, it will delete the mime file.
        
        tem_audio: Default `False`. If `True`, it will delete the audio file.
        """
        os.remove(f"Bilibili_scrape/data/{self.bvid}_playUrl.json")










