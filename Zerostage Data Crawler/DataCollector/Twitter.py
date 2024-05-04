#coding=utf-8
import datetime
import json
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup


# 个人信息接口：https://twitter.com/i/api/graphql/qW5u-DAuXpMEG0zA1F7UGQ/UserByScreenName?variables={"screen_name":"ogura_ari","withSafetyModeUserFields":true}&features={"hidden_profile_likes_enabled":true,"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}&fieldToggles={"withAuxiliaryUserLabels":false}

# 1.发送请求，获取网页框架以及main.js
# 2.提取main.js中UserTweets的id和特征等
# 3.根据id和特征，修改接口
# 4.发送获取前20个帖子的请求
# 5.剔除其中转推的帖子
# 6.统计帖子时间、评论、点赞、转推、展现数
# 7.统计该作者的粉丝数、简介
# 8.获取官网地址
class twitter:
    name = ""
    official_url = ""  # 官网url

    user_id = 0
    rest_id = ""
    user_feature = []
    tweets_id = 0
    tweets_feature = []

    twitter_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                       "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    main_headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Content-Type": "application/json",
        "Cookie": "_ga=GA1.2.1123922545.1678144025; mbox=session#e72d0f58a33d467b8de6df771df05a60#1686377705|PC#e72d0f58a33d467b8de6df771df05a60.38_0#1749620645; guest_id=v1%3A169332057977156245; guest_id_marketing=v1%3A169332057977156245; guest_id_ads=v1%3A169332057977156245; kdt=stHa3BZsH1RDY8v2nBoBwS3w2ZvvZS7A0sEN6ulR; auth_token=ae419ba06ab9e8b25529dc70eaff8ebc718af3a3; ct0=74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a; twid=u%3D1504337770407473153; _gid=GA1.2.535867160.1714643334; lang=zh-cn; personalization_id=\"v1_jy+V7csaWz8N5UCDeOc6nw==\"",
        "Priority": "u=1, i", "Referer": "https://twitter.com/ogura_ari",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Client-Transaction-Id": "Zdt9Sq6HnAgmUQO4etGzI45ZKJppkquCtShIl9qcURb50bL0R2xUAfBz5XXCHr0pFhR+gGSkGhUFIIQwFtRtHx62cFSeZg",
        "X-Client-Uuid": "0577685c-e2d1-4429-b4c0-62786f460eac",
        "X-Csrf-Token": "74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a",
        "X-Twitter-Active-User": "yes", "X-Twitter-Auth-Type": "OAuth2Session",
        "X-Twitter-Client-Language": "zh-cn"
    }
    info_headers = {"Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9",
                    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "Content-Type": "application/json",
                    "Cookie": "_ga=GA1.2.1123922545.1678144025; mbox=session#e72d0f58a33d467b8de6df771df05a60#1686377705|PC#e72d0f58a33d467b8de6df771df05a60.38_0#1749620645; guest_id=v1%3A169332057977156245; guest_id_marketing=v1%3A169332057977156245; guest_id_ads=v1%3A169332057977156245; kdt=stHa3BZsH1RDY8v2nBoBwS3w2ZvvZS7A0sEN6ulR; auth_token=ae419ba06ab9e8b25529dc70eaff8ebc718af3a3; ct0=74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a; twid=u%3D1504337770407473153; _gid=GA1.2.535867160.1714643334; lang=zh-cn; personalization_id=\"v1_FBy5/X378sW9AMH7IicLrw==\"",
                    "Priority": "u=1, i", "Referer": "https://twitter.com/ogura_ari",
                    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                    "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "X-Client-Transaction-Id": "mjlYc9xys4gsWNBA+FA0EHDjskszRXnvGV7iEq7MsKQtH0uMP0abI5YyAx42WPhKpKzQf5uBRgCD52r4mMo0vRakmZfomQ",
                    "X-Csrf-Token": "74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a",
                    "X-Twitter-Active-User": "yes", "X-Twitter-Auth-Type": "OAuth2Session",
                    "X-Twitter-Client-Language": "zh-cn"}
    tweets_headers = {"Accept": "*/*",
                      "Accept-Language": "zh-CN,zh;q=0.9",
                      "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                      "Content-Type": "application/json",
                      "Cookie": "_ga=GA1.2.1123922545.1678144025; mbox=session#e72d0f58a33d467b8de6df771df05a60#1686377705|PC#e72d0f58a33d467b8de6df771df05a60.38_0#1749620645; guest_id=v1%3A169332057977156245; guest_id_marketing=v1%3A169332057977156245; guest_id_ads=v1%3A169332057977156245; kdt=stHa3BZsH1RDY8v2nBoBwS3w2ZvvZS7A0sEN6ulR; auth_token=ae419ba06ab9e8b25529dc70eaff8ebc718af3a3; ct0=74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a; twid=u%3D1504337770407473153; _gid=GA1.2.535867160.1714643334; lang=zh-cn; personalization_id=\"v1_87W2rIRbUHjW1cL+t9fcrw==\"",
                      "Priority": "u=1, i", "Referer": "https://twitter.com/Polemos_io",
                      "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                      "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Dest": "empty",
                      "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                      "X-Client-Transaction-Id": "2/h2pCcQZul++n20ED3ZPLNHh2CDK/3JjvnQpvwuwbDpuiMOsOAYxy1+77Fw9dbrUkFIPtrHzThAe22lu9Sesmhygz5s2A",
                      "X-Client-Uuid": "0577685c-e2d1-4429-b4c0-62786f460eac",
                      "X-Csrf-Token": "74085fecaf2ee67e7f6b256c357bbea7ccc4904f3ebdff82106284c7ecf26232dad190cc9ded5668140c266aa7ab6f90dc589a4fea74d78632224cdcc04167482c562226f1df2f9659058c6e23031b2a",
                      "X-Twitter-Active-User": "yes", "X-Twitter-Auth-Type": "OAuth2Session",
                      "X-Twitter-Client-Language": "zh-cn"}

    url = ""  # 推特网址
    main_url = ""  # main.js接口
    info_url = "https://twitter.com/i/api/graphql/{user_id}/UserByScreenName?"  # 个人信息接口
    tweets_url = "https://twitter.com/i/api/graphql/{user_id}/UserTweets?"

    # 1.发送请求，获取网页框架以及main.js
    def request_twitter(self):
        self.name = self.url[self.url.rfind("/") + 1:]
        response = requests.get(self.url, headers=self.twitter_headers)
        web_struct = BeautifulSoup(response.text, 'lxml')
        script_list = web_struct.select("script")
        for i in script_list:
            e = i.attrs.get("src")
            if e != None and e.find("main") != -1:
                self.main_url = e

    # 获取个人信息（粉丝数、userid、简介）
    def get_info(self):
        # 构建接口，参数

        # 读取接口的基本参数
        JSON = json.loads(open("../info.json.py", "r").read())
        # 修改参数
        JSON["variables"]["screen_name"] = self.name
        for i in self.user_feature:
            JSON["features"][i] = "true"
        url = self.info_url.replace("{user_id}", self.user_id)
        # 构建接口（url）
        for e in list(JSON.keys()):
            url = url + e + "=" + json.dumps(JSON[e]) + "&"

        url = url[:len(url) - 1].replace(": ", ":").replace(", ", ",").replace("\"true\"", "true").replace("\"false\"",
                                                                                                           "false")
        # print(url)
        response = requests.get(url, headers=self.info_headers)
        # 解析，获取userid、粉丝数、简介
        JSON = json.loads(response.text)
        self.rest_id = JSON["data"]["user"]["result"]["rest_id"]
        # try:
        #     url_list = JSON["data"]["user"]["result"]["legacy"]["entities"]["url"]["urls"]
        #     # 查询官网网址
        #     for i in url_list:
        #         if str.lower(i["expanded_url"]).find(str.lower(self.name)) != -1:
        #             self.official_url = i["expanded_url"]
        #             break
        # except:
        #     pass

        followers_count = float(JSON["data"]["user"]["result"]["legacy"]["followers_count"])  # 粉丝数
        description = JSON["data"]["user"]["result"]["legacy"]["description"]  # 简介

        print(self.url)
        print(description)
        print(f"Followers:{self.num_format_def(followers_count, '.1f')}")
    # 2.提取main.js中有效信息
    def get_main(self):
        response = self.request(self.main_url)
        main = response.text.split("},")

        # 提取个人信息的编号和特征
        for i in main:
            if i.find("operationName:\"UserByScreenName\"") != -1:
                self.user_id = str(i[i.find("queryId") + 9:i.find("operationName") - 2])
                self.user_feature = i[i.find("featureSwitches") + 17:i.find("fieldToggles") - 2].replace("\"",
                                                                                                         "").split(",")
                break

        # 提取帖子的ID和特征
        user_tweets = ""
        for i in main:
            if i.find("operationName:\"UserTweets\"") != -1:
                user_tweets = i
                break

        # 帖子id
        self.tweets_id = user_tweets[user_tweets.find("queryId") + 9:user_tweets.find("operationName") - 2]
        # 帖子特征
        self.tweets_feature = user_tweets[
                              user_tweets.find("featureSwitches") + 17:user_tweets.find("fieldToggles") - 2].replace(
            "\"", "").split(",")

    # 获取帖子信息
    def get_tweets(self):
        # 读取json文件中url参数模板
        JSON = json.loads(open("../twitter.json", "r").read())
        JSON["variables"]["userId"] = self.rest_id
        for i in self.tweets_feature:
            JSON["features"][i] = "true"
        # print(JSON)

        # 将参数传入url
        url = self.tweets_url.replace("{user_id}", self.tweets_id)
        # 构建接口（url）
        for e in list(JSON.keys()):
            url = url + e + "=" + json.dumps(JSON[e]) + "&"

        url = url[:len(url) - 1].replace(": ", ":").replace(", ", ",").replace("\"true\"", "true").replace("\"false\"",
                                                                                                           "false")
        # print(url)

        # 获取json数据，解析帖子的信息
        response = requests.get(url, headers=self.tweets_headers)
        JSON = json.loads(response.text)
        temp_list = JSON["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
        tweets_list = []
        # print(type(temp_list))
        for i in temp_list:
            if "entries" in i:
                tweets_list = i["entries"]

        recent_time = None  # 记录最近时间
        latest_time = None  # 记录最迟发布时间
        tot_reply_count = float(0)  # 总评论数
        tot_favorite_count = float(0)  # 总点赞数
        tot_retweet_count = float(0)  # 总转发量
        tot_view_count = float(0)  # 总观看量
        count = 0  # 有效帖子数（非转载帖子）
        for i in tweets_list:
            if i["entryId"].find("tweet") == -1: continue  # 去掉非帖子的部分


            temp = i["content"]["itemContent"]["tweet_results"]["result"]  # 让temp包含该帖子的所有信息
            if "tweet" in temp:
                temp = temp["tweet"]
            # 判断是否为转帖的帖子

            if "count" not in temp["views"]: continue

            # 进行统计
            # 时间统计
            time = temp["legacy"]["created_at"]
            time = datetime.datetime.strptime(self.time_formot(time), "%m %d %H:%M:%S +0000 %Y")

            if recent_time == None:
                recent_time = time
            elif time > recent_time:
                recent_time = time
            if latest_time == None:
                latest_time = time
            elif time < latest_time:
                latest_time = time

            tot_view_count = tot_view_count + float(
                temp["views"]["count"])
            tot_favorite_count = tot_favorite_count + float(
                temp["legacy"]["favorite_count"])
            tot_reply_count = tot_reply_count + float(
                temp["legacy"]["reply_count"])
            tot_retweet_count = tot_retweet_count + float(
                temp["legacy"]["retweet_count"])
            count = count + 1
            # print(temp["legacy"])

        count=float(count)
        # 统计完成，进行平均数等数据计算
        time_interval=max(1,(recent_time-latest_time).days)  #计算最大间隔几天
        print(f"Average Messages per day:{self.num_format(count/time_interval)}")
        print(f"Average Comment per post:{self.num_format(tot_reply_count/count)}")
        print(f"Average Retweet per post:{self.num_format(tot_retweet_count/count)}")
        print(f"Average Like per post:{self.num_format(tot_favorite_count/count)}")
        print(f"Average Views per post:{self.num_format(tot_view_count/count)}")

    # 格式转换，若大于1000，则转化为k表示，否则四舍五入(保留几位小数自定义)
    def num_format_def(self,num,format):
        if num<1:
            return "<1"
        if num>1000:
            num=num/1000
            return str(num.__format__(format))+"k"
        return num.__format__(format)

    #格式转换，若大于1000，则转化为k表示，否则四舍五入
    def num_format(self,num):
        if num<1:
            return "<1"
        if num>1000:
            num=num/1000
            return str(num.__format__(".0f"))+"k"
        return num.__format__(".0f")
    def request(self, url):
        response = requests.get(url=url, headers=self.main_headers)
        return response

    def __init__(self, url):
        self.url = url

    def exec(self):
        self.request_twitter()
        self.get_main()
        self.get_info()
        self.get_tweets()

    def time_formot(self, string):
        date = {'Jan':'01',
                'Feb':'02',
                'Mar':'03',
                'Apr':'04',
                'May':'05',
                'Jun':'06',
                'Jul':'07',
                'Aug':'08',
                'Sep':'09',
                'Oct':'10',
                'Nov':'11',
                'Dec':'12'}
        string = string[4:]
        for i in list(date.keys()):
            string=string.replace(i,date[i])
        return string


if __name__ == '__main__':
    print("输入推特网址")
    url = input()
    twitter(url).exec()
