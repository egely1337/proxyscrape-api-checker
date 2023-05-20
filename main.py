#Author: egely1337
#Date: 1/3/2023

from requests import get
from threading import Thread
from util.log import *
from time import sleep
import math

api_url = "https://httpbin.org/ip"
proxyscrape_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all"
good_proxies = []
mid_proxies = []
bad_proxies = []
tried = 0

def get_proxies_from_api():
    global proxies
    try:
        r = get(url=proxyscrape_api_url)
        list = r.text.split("\n")
        log_green("Got {} proxies from api".format(len(list)))
        return list
    except:
        log_red("Failed to get proxies from api")
        pass

def test_proxy(proxy: str):
    global tried
    try:
        prxy = {"https" : "http://{}".format(proxy.strip())}
        r = get(url=api_url, proxies=prxy, timeout=15)
        ping = math.ceil(r.elapsed.total_seconds()*1000)
        if(r.json().get("origin") != proxy):
            if ping < 5000:
                good_proxies.append(proxy)
            elif ping < 15000:
                mid_proxies.append(proxy)
            else:
                bad_proxies.append(proxy)
            log_green(f"Proxy is working: {proxy[:-1]:<30}Ping: {ping} ms")
            tried = tried + 1
    except:
        just_log("Proxy is not working: {}".format(proxy[:-1]))
        tried = tried + 1
        pass

def write_proxies(proxy_list, quality) -> None:
    try:
        fp = open(f"{quality}.txt", mode="w", encoding="utf-8")
        for i in proxy_list:
            fp.write(i)
        fp.close()
        log_green("Wrote {} {}".format(len(proxy_list), quality))
    except Exception as e:
        print(e)
        log_red("Failed to write proxies")
        pass

def main() -> None:
    proxy_list = get_proxies_from_api()
    p_len = len(proxy_list)
    log_green("Loaded {} proxies!".format(p_len))
    for i in proxy_list:
        thread = Thread(target=test_proxy, args=(i,))
        thread.start()

    #Wait till the process completed
    while tried < p_len:
        sleep(1) #for cpu saving
    write_proxies(good_proxies, "!good_proxies")
    write_proxies(mid_proxies, "!mid_proxies")
    write_proxies(bad_proxies, "!bad_proxies")

main()
