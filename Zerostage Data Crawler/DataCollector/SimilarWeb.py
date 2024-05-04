import datetime
import json

import requests


# Similiar的总访问量接口：
# https://pro.similarweb.com/widgetApi/WebsiteOverview/EngagementVisits/Graph?country=999&from=2024%7C01%7C01&to=2024%7C03%7C31&timeGranularity=Monthly&ShouldGetVerifiedData=false&includeSubDomains=true&isWindow=false&keys=easya.io&webSource=Total

# Similiar的地理接口
# https://pro.similarweb.com/widgetApi/WebsiteGeography/Geography/Table?country=999&includeSubDomains=true&webSource=Total&timeGranularity=Monthly&orderBy=TotalShare%20desc&keys=tashi.gg&pageSize=5&from=2024%7C01%7C01&to=2024%7C03%7C31&isWindow=false

class Similarweb:
    similarweb_header = {}
    similarweb_url = ""
    # 请求总访问量的接口
    visit_base_url = "https://pro.similarweb.com/widgetApi/WebsiteOverview/EngagementVisits/Graph?country=999&from={startTime}&to={endTime}&timeGranularity=Monthly&ShouldGetVerifiedData=false&includeSubDomains=true&isWindow=false&keys={webUrl}&webSource=Total"
    # 请求热门国家/地区的接口
    geo_base_url = "https://pro.similarweb.com/widgetApi/WebsiteGeography/Geography/Table?country=999&includeSubDomains=true&webSource=Total&timeGranularity=Monthly&orderBy=TotalShare%20desc&keys={webUrl}&pageSize=5&from={startTime}&to={endTime}&isWindow=false"

    start_time = ""
    end_time = ""

    # 测试当前日期是否可用，不可用的话，将日期更换为上一个月到三个月前，若还不行，则改为前两个月到五个月前
    def testData(self):

        # 先以当前设置的日期发送一次
        test_url = self.visit_base_url.replace("{startTime}", self.start_time).replace("{endTime}",
                                                                                       self.end_time).replace(
            "{webUrl}", self.similarweb_url)

        response = self.request(test_url)
        if (response.status_code != 200):
            # 将日期更换为上一个月到三个月前

            now = datetime.datetime.today()  # 获取今日日期
            new_start_time = now.replace(month=now.month - 3).replace(day=1).strftime("%Y|%m|%d")  # 新开始日期为三个月前
            new_end_time = (now.replace(month=now.month) - datetime.timedelta(days=now.day)).strftime("%Y|%m|%d")  # 新结束日期为一个月前
            test_url = self.visit_base_url.replace("{startTime}", new_start_time).replace("{endTime}",
                                                                                          new_end_time).replace(
                "{webUrl}", self.similarweb_url)
            response = self.request(test_url)
            if (response.status_code != 200):
                # 改为前两个月到五个月前
                new_start_time = now.replace(month=now.month - 4).replace(day=1).strftime("%Y|%m|%d")  # 新开始日期为四个月前，月初
                new_end_time = (now.replace(month=now.month - 1) - datetime.timedelta(days=now.day)).strftime(
                    "%Y|%m|%d")  # 新结束日期为两个月前，月末
                test_url = self.visit_base_url.replace("{startTime}", new_start_time).replace("{endTime}",
                                                                                              new_end_time).replace(
                    "{webUrl}", self.similarweb_url)
                response = self.request(test_url)
                if(response.status_code!=200):
                    print("日期有问题，请修改time.json")
                    return False
            # 将发送日期更新为有效的
            self.start_time = new_start_time
            self.end_time = new_end_time
            JSON=dict()
            JSON["startTime"]=self.start_time
            JSON["endTime"]=self.end_time
            with open("../time.json", "w") as file:
                file.write(json.dumps(JSON))
            file.close()
        return True

    # 输入官网网址，获取官网名
    def get_web_name(self,url):
        url=url.replace("www.","")
        self.similarweb_url = url[url.find("//") + 2:url.rfind("/")]

    def __init__(self, web_url):
        self.get_web_name(web_url)

        self.readHeader()
        self.readTime()

    def readTime(self):
        JSON = json.loads(open("../time.json", "r").read())
        self.start_time = JSON["startTime"].replace("/", "%7C")
        self.end_time = JSON["endTime"].replace("/", "%7C")

    # 读入请求头
    def readHeader(self):
        self.similarweb_header = json.loads(open("../headers.json", "r").read())

    # 重新设置json文件中的Cookie属性
    def resetCookie(self):
        print("输入新的cookie")
        print()
        new_cookie = input()
        self.similarweb_header["Cookie"] = new_cookie
        with open("../headers.json", "w") as file:
            file.write(json.dumps(self.similarweb_header))
        file.close()

    # 发送请求
    def request(self, url):
        return requests.get(url=url, headers=self.similarweb_header)

    # 解析总访问量
    def analize_visit_num(self):

        url = self.visit_base_url.replace("{startTime}", self.start_time).replace("{endTime}", self.end_time).replace(
            "{webUrl}", self.similarweb_url)
        # 发送请求
        response = self.request(url)
        while (response.status_code != 200):
            print("请求失败，可能是cookie过期")
            self.resetCookie()
            response = self.request(url)

        # 解析返回的json数据，形成列表
        list = json.loads(response.text)["Data"][self.similarweb_url]["Total"][0]

        # 将列表中的数据相加，转为对应格式
        count = float(0)
        number=0
        for i in list:
            if i["Value"]==None:
                continue
            count = count + float(i["Value"])
            number=number+1
        count = count / float(number)
        count = count / 1000

        print(f"avg monthly visit:{format(count, '.2f')}K")

    # 解析各地区占比
    def analize_geo(self):
        url = self.geo_base_url.replace("{startTime}", self.start_time).replace("{endTime}", self.end_time).replace(
            "{webUrl}", self.similarweb_url)
        # 发送请求
        response = self.request(url)
        while (response.status_code != 200):
            print("请求失败，可能是cookie过期")
            self.resetCookie()
            response = self.request(url)

        # 解析返回的json数据，形成列表
        country_list = json.loads(response.text)["Filters"]["country"]  # 城市编号->城市名映射列表

        data_list = json.loads(response.text)["Data"]  # 城市编号及该城市占比列表

        # 让data_list存储城市名以及占比
        for i in range(5):
            for j in country_list:
                if (int(j["id"]) == data_list[i]["Country"]):
                    data_list[i]["Country"] = j["text"].replace("United States", "USA").replace("United Kingdom", "UK")

        for i in range(3):
            print(data_list[i]["Country"] + ":" + format(data_list[i]["Share"] * 100, '.0f') + "%", end=" ")


    def exec(self):
        if self.similarweb_url=="":
            return
        if(self.testData()==False):
            return
        web="https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/{startTime}-{endTime}?webSource=Total&key={web_url}"
        web=web.replace("{startTime}",self.start_time[:7]).replace("{endTime}",self.end_time[:7]).replace("{web_url}",self.similarweb_url).replace("|",".")
        print(web)
        self.analize_visit_num()
        self.analize_geo()
        print()


if __name__ == '__main__':
    # Similarweb部分
    print("输入官网网址")
    official_url = input()
    ee = Similarweb(official_url)
    ee.exec()


