import requests
import configparser
from abc import ABC, abstractmethod
import json
from linebot.models import (
    CarouselColumn,
    URITemplateAction
)
config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('weather', 'WEATHER_TOKEN')

# 天氣抽象類別
class Weather(ABC):
    def __init__(self):
        pass

    def get(self):
        pass

# 中央氣象局
class CWB(Weather): 
    def __init__(self, city):
        self.city = city

    def get(self):
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' +\
                token + '&format=JSON&locationName=' + self.city
        Data = requests.get(url)
        text = Data.text.encode('utf-8')
        Data = (json.loads(text))['records']['location'][0]['weatherElement']
        res = [[] for _ in range(3)]
        for j in range(3):
            for i in Data:
                res[j].append(i['time'][j])
        
        weather = [CarouselColumn(
            thumbnail_image_url='https://i.imgur.com/yOgAsKx.jpg',
            title = '{} ~ {}'.format(data[0]['startTime'][5:-3], data[0]['endTime'][5:-3]),
            text = '天氣狀況\t{}\n溫度\t{} ~ {} °C\n降雨機率\t{} %'.format(
                data[0]['parameter']['parameterName'], 
                data[2]['parameter']['parameterName'], 
                data[4]['parameter']['parameterName'], 
                data[1]['parameter']['parameterName']),
            actions = [
                URITemplateAction(
                    label = '詳細內容',
                    uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                )
            ]
        ) for data in res]
        
        return weather