
#encoding=utf-8
import requests
from bs4 import BeautifulSoup
class Telegram:
    url=""
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9", "Cache-Control": "max-age=0",
        # "Cookie": "stel_ssid=2962cd9d5ef4d0cd37_2020245149406914223", "Priority": "u=0, i",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    def __init__(self,url):
        self.url=url

    def analize(self):
        response=requests.get(url=self.url,headers=self.header)
        web_struct=BeautifulSoup(response.text,"lxml")
        # print(web_struct)
        div=web_struct.select(".tgme_page_extra")[0].text
        try:
            followers = (float(div[:div.find("members")].replace(' ', '')) / 1000).__format__(".1f")
            online = (float(div[div.find(",") + 1:div.find("online")].replace(' ', '')) / 1000).__format__(".1f")
        except:
            followers = (float(div[:div.find("subscriber")].replace(' ', '')) / 1000).__format__(".1f")
            online = 0
        print(self.url)
        print(f'Followers:{followers}k')
        print(f"Online:{online}k")

    def exec(self):
        if self.url=="":
            return
        self.analize()


if __name__ == '__main__':
    print("输入Telegram")
    url = input()
    Telegram(url).exec()