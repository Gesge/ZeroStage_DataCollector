# twitterScore网址的接口：https://twitterscore.io/twitter/{用户名}/overview/
import requests
from bs4 import BeautifulSoup


class twitter_score:
    twitter_header = {
        "Accept": "text/html,application/xhtml+xmdasf asd asdl,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "csrftoken=Ux8g2rmQp5Sj9ZJqF4dzpm6F04XujEAzui8UvrgxPUF5xvu5J3NQMZ2yt0irMKtc; _ga=GA1.1.1548320859.1714466804; _hjSession_3071534=eyJpZCI6IjYwYjlmZDE2LTU5YWUtNDQ1Zi1iZTE3LTA4YmE3MjRmZDY5MCIsImMiOjE3MTQ0NjY4MDQwNTksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _ym_uid=1714466807375638839; _ym_d=1714466807; _ym_isad=1; _ym_visorc=w; _hjSessionUser_3071534=eyJpZCI6ImNjNjgwNDc4LTJlMzktNTJlYy1hZWQxLWM0ODZhYjRkNTU3NSIsImNyZWF0ZWQiOjE3MTQ0NjY4MDQwNTksImV4aXN0aW5nIjp0cnVlfQ==; sessionid=eo7go1qvhr1ks6jzgj0gqyu0yzgx61it; _ga_QK3YK5CHT8=GS1.1.1714466803.1.1.1714468828.0.0.0",
        "Priority": "u=0, i", "Referer": "https://twitterscore.io/",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    def __init__(self, twitter_url):
        self.twitter_url = twitter_url
        self.twitter_score_url = "https://twitterscore.io/twitter/{用户名}/overview/".replace("{用户名}", twitter_url[
                                                                                                          twitter_url.rfind(
                                                                                                              "/") + 1:])

    def analize_web(self):
        response = requests.get(url=self.twitter_score_url, headers=self.twitter_header)
        if (response.status_code == 404):
            print("返回404，估计名气太小，找不到该用户")
            return
        web_struct = BeautifulSoup(response.text, 'lxml')  # 将网页放入解析
        # 获取评价以及Score信息
        count_wrapper = web_struct.select(".count-wrapper")[0]  # 获取包含评价以及评分的标签
        script_list=web_struct.select("script")
        score=""
        for script in script_list:
            if str(script).find('const text') != -1:
                e=str(script)
                list=e.split(";")
                for i in list:
                    if i.find("const text")!= -1:
                        score=i[i.find("Score")+9:i.rfind("!")]


        evaluate = count_wrapper.select("p")[0].text
        # score = count_wrapper.select(".followersCountInside")[0].text
        print(f"评价：{evaluate}")
        print(self.twitter_score_url)
        print(f"Score:{score}")

    def exec(self):
        if self.twitter_url=="":
            return
        self.analize_web()

if __name__ == '__main__':
    # TwitterScore部分
    print("输入推特网址")
    twitter_url = input()

    twitter_score(twitter_url).exec()


