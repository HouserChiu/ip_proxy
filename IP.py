#ip代理写法，先在Terminal里面运行代理池，然后修改爬虫代码


import requests

url = 'https://www.zhipin.com/chengdu/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

#代理的接口
proxy_pool_url = 'http://127.0.0.1:5000/get'

#开始设置代理为空，全局变量，代理好用，一直延用，不需要来回传
proxy = None
#确保不进行死循环
max_count = 5

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            #网页返回的内容就是代理的内容
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    #打印调试信息
    print("Crawling", url)
    print("Trying Count", count)
    global proxy
    if count >= max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            #requests获取代理的方法
            proxies = {
                "http": "http://" + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            #需要代理
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print("Get Proxy Failed")
                return None
    except ConnectionError as e:
        print("Error Occured", e.args)

        proxy = get_proxy()
        count += 1
        return get_html(url, count)
