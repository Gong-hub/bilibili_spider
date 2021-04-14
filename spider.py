# _*_ coding: utf-8 _*_
# @Project_Name : bilibili_spider
# @Time         : 2021/4/13 19:11
# @Author       : Gong-hub
# @Email        : 2821813806@qq.com
# @File         : spider.py
# @Software     : PyCharm
import requests, logging, json, time
from pymongo import MongoClient


def request(url,**kwargs):
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    t = 0
    while t <= 3:
        response = requests.get(url=url,headers=headers,params=kwargs["params"])
        if response.status_code == 200:
            rs_json = response.json()
            if rs_json['code'] == 0:
                return rs_json
            else:
                logging.info("第{}次访问成功，服务器返回状态码错误，错误信息{}。。。".format(t+1,rs_json["message"]))
                t += 1
                continue
        else:
            logging.info("第{}次访问失败,正在重试...".format(t+1))
            t += 1
            continue
    raise

def loadconfig():
    return json.loads("config.json")


def insert_one(data):
    db = client["bili"]
    db['user_info'].insert_one(data)
    logging.info("")

def fans_spider():
    url = "http://api.bilibili.com/x/web-interface/card"
    for user_uid in config['user_list']:
        params = {
            "mid": user_uid
        }
        rs_json_data = request(url,params=params)
        yield {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "data": rs_json_data}


def main():
    for data in fans_spider():
        insert_one(data)
    pass

if __name__ == '__main__':
    config = loadconfig()
    client = MongoClient(config['mongoclint'])
    main()
