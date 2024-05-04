import json

import requests


# 接口：https://discord.com/api/v9/invites/{名}?with_counts=true&with_expiration=true
class discord:
    base_url=""
    name=""
    online_url="https://discord.com/api/v9/invites/{名}?with_counts=true&with_expiration=true"

    def __init__(self,url):
        self.base_url=url
        self.name=url[url.find("invite")+7:]
        self.online_url=self.online_url.replace("{名}",self.name)

    def analize(self):
        response=requests.get(url=self.online_url)
        list=json.loads(response.text)
        followers=(float(list['approximate_member_count'])/1000).__format__(".1f")
        online=(float(list["approximate_presence_count"])/1000).__format__(".1f")
        print(self.base_url)
        # print()
        print(f'Followers:{followers}k')
        print(f"Online:{online}k")

    def exec(self):
        if self.base_url=="":
            return
        self.analize()


if __name__ == '__main__':
    print("输入discord")
    url=input()
    discord(url).exec()