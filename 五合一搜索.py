from Discord import discord
from TwitterScore import twitter_score
from SimilarWeb import Similarweb
from Telegram import Telegram
from Twitter import twitter

if __name__ == '__main__':
    # TwitterScore部分
    print("请输入推特网址:")
    twitter_url = input()
    # Similarweb部分
    print("Smilarweb - 输入官网网址:")
    official_url = input()
    # 电报群部分
    print("输入Telegram网址:")
    telegram_url = input()
    # DC社群部分
    print("输入discord网址：")
    discord_url = input()

    # 执行
    print()
    print("************爬取并分析数据ing************")
    print()
    print("---Twitter数据结果：")
    twitter(twitter_url).exec()
    print()
    twitter_score(twitter_url).exec()
    print()
    print("---官网数据结果：")
    Similarweb(official_url).exec()
    print()
    print("---TG粉丝数和在线人数：")
    Telegram(telegram_url).exec()
    print()
    print("---DC粉丝数和在线人数：")
    discord(discord_url).exec()


