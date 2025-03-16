from tqdm import tqdm
import requests
import dotenv

def load_cookie(*keys) -> dict:
    '''
    Return
    ----------
    {"cookie": cookie}
    '''
    cookies = dotenv.dotenv_values("Bilibili_scrape/data/cookie.env")
    cookie_string = ""
    if keys:
        try:
            for key in keys:
                cookie_string += f"{key}={cookies[key]};"
        except KeyError:
            string = f'''There are errors in your params. The keys that you can use contain: {set(cookies.keys())}'''

            return string
    else:
        for key, value in cookies.items():
            cookie_string += f"{key}={value};" 
    
    return {"cookie": cookie_string}

def load_headers(*headers) -> dict:
    """
    Params
    ----------
    headers: HTTP headers that you need to use.
        In this function, it has "user-agent", "regerer"
    """
    headers_meta = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "referer" : "https://www.bilibili.com/"
    }
    headers_return = dict()
    if headers:
        for item in headers:
            headers_return[item] = headers_meta[item]
        return headers_return
    else:
        return headers_meta

def downloader(url:str, type:str, path):
    if type == "mp3":
        file_name = "audio"
    elif type == "mp4":
        file_name = "video"
    response = requests.get(url, headers=load_headers(), cookies=load_cookie(), stream=True)
    if response.status_code == requests.codes.OK:
        with open(f"{path}/{file_name}.{type}", 'wb') as f:
            with tqdm(desc=f"{file_name}.{type}:", total=float(response.headers.get("content-length", 0)), unit="B", unit_scale=True, unit_divisor=1024) as bar:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
                    bar.update(len(chunk))
    else:
        print(f"Connect failed. Status code: {response.status_code}")





