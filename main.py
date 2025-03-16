import requests
import json
import re
import ffmpeg
import sys
import utils
import login

def check_login_status():
    check_loginStatus_url = "https://api.bilibili.com/x/space/user/setting/list"
    try:
        check_loginStatus_response = requests.get(url=check_loginStatus_url, headers=utils.load_headers("user-agent"), cookies=utils.load_cookie())
        if check_loginStatus_response.status_code == requests.codes.OK:
            check_loginStatus_response = check_loginStatus_response.text
            if json.loads(check_loginStatus_response)['code'] == 0:
                print("The cookie of user is OK.")
            else:
                login.login_QRcode() 
        else:
            print(f"The request to check login status is wrong. The status code is {check_loginStatus_response.status_code}")
            sys.exit()
    except:
        print("There is an unknown error when check the login status.")
        sys.exit()


def download(url:str, video_need:bool=True, audio_need=True, remove_tem_video:bool=False, remove_tem_audio:bool=False):
    """
    Download the video from Bilibili's video source url

    Params
    ----------
    video_need: Default `True`. If `False`, it will not download this media.
    
    audio_need: Default `True`. If `False`, it will not download this media.
    
    remove_tem_video: Default `False`. If `True`, it will delete the mime.
    
    remove_tem_audio: Default `False`. If `True`, it will delete the audio.
    """
    import video

    url_target: str = url
    response = requests.get(url=url_target, headers=utils.load_headers("user-agent"), cookies=utils.load_cookie()).text
    aid = re.search(r'"aid":(\d+)', response)[1]
    bvid = re.search(r'"bvid":"(.+?)"', response)[1]
    cid = re.search(r'"cid":(\d+)', response)[1]

    info = video.videoInfo(aid, bvid)
    play_url = video.videoPlayUrl(aid, bvid, cid)
    title = info.title()
    print(f"现在在下载：{title}")
    if video_need: # 下载无声视频
        utils.downloader(play_url.video_source_url(), "mp4", title)
    if audio_need: # 下载音频
        utils.downloader(play_url.audio_source_url(), "mp3", title)
    if video_need and audio_need == True:
        video = ffmpeg.input(f"{title}/video.mp4")
        audio = ffmpeg.input(f"{title}/audio.mp3")
        output = ffmpeg.output(video, audio, f"{title}/{title}.mp4")
        ffmpeg.run(output)
    info.delete_temporary_file()
    if video_need and remove_tem_video == True:
        remove_tem_video = True
    if audio_need and remove_tem_audio == True:
        remove_tem_audio = True
    play_url.delete_temporary_file(tem_video=remove_tem_video, tem_audio=remove_tem_audio)


if __name__ == "__main__":
    check_login_status()
    link_list:list = [

    ]
    count:int = 0
    for i in link_list:
        count += 1
        wait_num:int = len(link_list)
        download(i, video_need=True, audio_need=False, remove_tem_video=True, remove_tem_audio=True)
        print(f"----------现在还剩{wait_num - count}个----------")


"""
检查清单：
1、是否下载无声视频：
2、是否下载音频：
3、是否在将无声视频与音频合并后删除无声视频：
4、是否在将无声视频与音频合并后删除音频：
5、是否希望自己指定下载的视频清晰度
6、是否希望自己指定下载的音频品质
"""

