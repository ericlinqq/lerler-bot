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
                token + '&format=JSON&locationName=' + str(self.city)
        Data = requests.get(url)
        text = Data.text.encode('utf-8')
        Data = (json.loads(text))['records']['location'][0]['weatherElement']
        res = json.load(open('card.json', 'r', encoding='utf-8')) 

        for j in range(3):
            bubble = json.load(open('bubble.json','r',encoding='utf-8'))
            # title
            bubble['body']['contents'][0]['text'] = str(self.city) + '未來 36 小時天氣'
            # time
            bubble['body']['contents'][1]['contents'][0]['text'] = '{} ~ {}'.format(Data[0]['time'][j]['startTime'][5:-3],Data[0]['time'][j]['endTime'][5:-3])
            # weather
            bubble['body']['contents'][3]['contents'][0]['contents'][1]['text'] = Data[0]['time'][j]['parameter']['parameterName']
            # temp
            bubble['body']['contents'][3]['contents'][1]['contents'][1]['text'] = '{}°C ~ {}°C'.format(Data[2]['time'][j]['parameter']['parameterName'],Data[4]['time'][j]['parameter']['parameterName'])
            # rain
            bubble['body']['contents'][3]['contents'][2]['contents'][1]['text'] = Data[1]['time'][j]['parameter']['parameterName'] + '%'
            # comfort
            bubble['body']['contents'][3]['contents'][3]['contents'][1]['text'] = Data[3]['time'][j]['parameter']['parameterName']
            res['contents'].append(bubble)
     
        return res 