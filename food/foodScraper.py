from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import json
import math
from urllib.parse import quote
import requests


# 美食抽象類別
class Food(ABC):

    def __init__(self, area, category, price):
        self.area = area # 地區
        self.category = category # 美食類別
        self.price = price #消費金額

    @abstractmethod
    def scrape(self):
        pass

# 愛食記爬蟲
class IFoodie(Food):
    
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area + 
            "/list/" + self.category + 
            "?priceLevel=" + self.price +
            "&sortby=popular&opening=true")

        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前十筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-558691085 restaurant-info'}, limit=10)
        
        if not cards:
            return ''

        # content = ""
        
        res = json.load(open('./card.json', 'r', encoding='utf-8'))
        count = 0
        # restaurants = []
        for card in cards:
            bubble = json.load(open('food/bubble.json', 'r', encoding='utf-8'))

            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-558691085 title-text"}).getText()
            split_title = title.split(' ')[0]

            try:
                rating = card.find(  # 餐廳評價
                    "div", {"class": "jsx-1207467136 text"}).getText()
            except AttributeError:
                rating = '無'
                pass

            if count < 2:
                image = card.find("img")['src']
            else: 
                image = card.find("img")['data-src']

            avg_price = card.find(  # 平均消費
                "div", {"class": "jsx-558691085 avg-price"}).getText()[5:]
            
            address = card.find(  #餐廳地址
                "div", {"class": "jsx-558691085 address-row"}).getText()
            
            url = 'https://ifoodie.tw' + card.find(  # 餐廳愛食記網址
                "a", {"class": "jsx-558691085"})['href']
            
            bubble['hero']['url'] = image
            bubble['body']['contents'][0]['text'] = title

            if rating != '無':
                for i in range(math.floor(float(rating))):
                    bubble['body']['contents'][1]['contents'][i]['url'] = 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png'

            bubble['body']['contents'][1]['contents'][5]['text'] = rating
           
            bubble['body']['contents'][2]['contents'][0]['contents'][0]['text'] = avg_price
            bubble['body']['contents'][3]['contents'][0]['contents'][0]['text'] = address
            bubble['footer']['contents'][0]['action']['uri'] = url
            bubble['footer']['contents'][1]['action']['uri'] = 'https://www.google.com.tw/maps/search/' + quote(split_title+address)
            bubble['footer']['contents'][2]['action']['displayText'] = '我覺得【' + title + '】不錯'
          
            
            res['contents'].append(bubble)
            count += 1
           
        return res
        