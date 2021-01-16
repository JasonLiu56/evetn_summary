import requests
from fake_useragent import UserAgent


ua = UserAgent()


def get_proxy():
    return requests.get("http://localhost:5010/get/").json()


def get_all_proxy():
    return requests.get("http://localhost:5010/get_all/")


def delete_proxy(proxy):
    requests.get("http://localhost:5010/delete/?proxy={}".format(proxy))


def getHtml(url):
    # ....
    retry_count = 2
    headers = {'User_Agent': str(ua.random)}
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=2)
            if html.status_code != 200:
                print("删除代理:{}".format(proxy))
                delete_proxy(proxy)
                return None

            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    print("删除代理:{}".format(proxy))
    delete_proxy(proxy)
    return None