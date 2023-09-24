import requests
import re
import json
import time
import datetime
from html.parser import HTMLParser
import random


def findidHash(string):
    pattern = r"start_youtube(.*?)ads-start"
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None
def findUsername(string):
    pattern = r"user-block-info-username\">(.*?)<"
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None

def findRating(string):
    pattern = r'Мой рейтинг: (\d+\.\d+)'
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None

def findBalance(string):
    match = re.search(r'id="new-money-ballans">([\d.]+)\sруб\.', string)
    if match:
        found_text = match.group(1).split()
        return found_text[0]
    else:
        return None
        
def findMoney(string):
    pattern = r'\d+\.\d+'
    match = re.findall(pattern, string)
    if match:
        return match[1]
    else:
        return None

def findData(html):
    match = re.search(r'data-meta="[^"]*?([^?"]+)"', html)
    if match:
        return match.group(1)
    else:
        return None
def currentTime():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S, %m/%d/%Y")
    return formatted_time
cookies = input("Nhap cookie: ")

userAgent = input("Nhap user agent: ")
# proxy = input("Nhap proxy(http://user:pass@ip:port): ")
# proxies = {
#     'http': proxy,
#     'https': proxy,
# }

headers1 = {
    'authority': 'aviso.bz',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': cookies,
    'referer': 'https://aviso.bz/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': userAgent,
    'x-requested-with': 'XMLHttpRequest',
}

headers2 = {
    'authority': 'aviso.bz',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': cookies,
    'origin': 'https://aviso.bz',
    'referer': 'https://aviso.bz/work-youtube',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': userAgent,
    'x-requested-with': 'XMLHttpRequest',
}
headers3 = {
    'authority': 'aviso.bz',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://skyhome.squarespace.com',
    'referer': 'https://skyhome.squarespace.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': userAgent,
}
count = 0
while True:
    response1 = requests.get('https://aviso.bz/work-youtube', headers=headers1)

    response1_txt = str(response1.text)
    userName = findUsername(response1_txt)
    rate = findRating(response1_txt)
    balance = findBalance(response1_txt)
    if userName == None or rate == None or balance == None:
        print("Cookie die!")
        break
    print("[" + userName + "] " + currentTime() + " | Rate: " + rate + " | Balance: " + balance + " RUB", end=" | ")
    idHash = findidHash(response1_txt)
    if idHash == None:
        print("Het job, nghi 10 phut!")
        time.sleep(600)
        continue
    id = idHash.split(",")[0].split('(')[1]
    hash = idHash.split(",")[1].split('\'')[1]

    data2 = {
        'id': id,
        'hash': hash,
        'func': 'ads-start',
        'user_response': '',
        'count_captcha_subscribe': '',
        'checkStepOneCaptchaSubscribe': 'false',
        'visitor_id': '',
        'request_id': '',
    }

    response2 = requests.post('https://aviso.bz/ajax/earnings/ajax-youtube.php', headers=headers2, data=data2)
    data = json.loads(response2.text)
    allData = findData(data['html'])
    video_id = allData.split("&")[0].split("=")[1]
    timer = allData.split("&")[1].split("=")[1]
    random_time1 = ''.join(random.choice('0123456789') for _ in range(15))
    random_time2 = ''.join(random.choice('0123456789') for _ in range(15))
    player_time = timer + '.' + random_time1
    report_id = allData.split("&")[2].split("=")[1]
    task_id = allData.split("&")[3].split("=")[1]
    hash = allData.split("&")[4].split("=")[1]

    data3 = {
        'hash': hash,
        'report_id': report_id,
        'task_id': task_id,
        'timer': timer,
        'player_time': player_time,
        'video_id': video_id,
        'playerState': '1',
        'stage': '2',
    }
    count+=1
    response3 = requests.post('https://aviso.bz/ajax/earnings/ajax-youtube-external.php', headers=headers3, data=data3)
    # response3_txt = response3.text
    # new_hash = response3_txt.split("&")[4][5:]
    # data4 = {
    #     'hash': new_hash,
    #     'report_id': report_id,
    #     'task_id': task_id,
    #     'timer': '3',
    #     'player_time': "2." + random_time2,
    #     'video_id': video_id,
    #     'playerState': '1',
    #     'stage': '2',
    # }
    # response4 = requests.post('https://aviso.bz/ajax/earnings/ajax-youtube-external.php', headers=headers3, data=data4)
    money = findMoney(response3.text)
    if money == None:
        print("=> Error")
        break
    else: print("+"+ money + " rub")
