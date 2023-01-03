#Author: egely1337
#Date: 1/3/2023

from requests import get
from threading import Thread
from util.log import *
from time import sleep

api_url = "https://httpbin.org/ip"
proxyscrape_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all"
success_proxies = []
tried = 0

def get_proxies_from_api() -> None:
    try:
        r = get(url=proxyscrape_api_url)
        list = r.text.split("\n")
        log_green("Got {} proxies from api".format(len(list)))
        fp = open("proxies",mode="w", encoding="utf-8")
        for i in list:
            fp.write(str(i))
        fp.close()
    except:
        pass
    


def load_proxies() -> list[str]:
    r = []
    fp = open("proxies", mode="r", encoding="utf-8")
    for line in fp:
        r.append(line)
    log_green("Loaded {} proxies!".format(len(r)))
    fp.close()
    return r

def test_proxy(proxy: str):
    global tried
    try:
        prxy = {"https" : "http://{}".format(proxy)}
        r = get(url=api_url, proxies=prxy, timeout=15)
        if(r.json().get("origin") != None):
            success_proxies.append(proxy)
            log_green("Proxy is working: {}".format(proxy[:-1]))
            tried = tried + 1
    except:
        tried = tried + 1
        pass

def write_proxies() -> None:
    try:
        fp = open("proxies", mode="w", encoding="utf-8")
        for i in success_proxies:
            fp.write(i)
        fp.close()
        log_green("Writed {} proxies".format(len(success_proxies)))
    except:
        pass

def main() -> None:
    get_proxies_from_api()
    proxies = load_proxies()
    p_len = len(proxies)
    for i in range(len(proxies)):
        thread = Thread(target=test_proxy, args=(proxies[i],))
        thread.start()

    #Wait till the process completed
    while tried < p_len:
        sleep(1) #for cpu saving
    write_proxies()

main()
