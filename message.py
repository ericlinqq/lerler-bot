from abc import ABC, abstractmethod
import json

# 訊息抽象類別
class Message(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def content(self):
        pass

# 「選擇地區」按鈕樣板訊息
class AreaMessage(Message):
    def content(self):

        body = json.load(open('food/button.json', 'r', encoding='utf-8'))
        body['hero']['url'] = 'https://i.imgur.com/5Ka5gah.jpg'

        return body

# 「選擇美食類別」按鈕樣板訊息
class CategoryMessage(Message):
    def __init__(self, area):
        self.area = area
    
    def content(self):
       
        body = json.load(open('food/button.json', 'r', encoding='utf-8'))
        body['hero']['url'] = 'https://i.imgur.com/8XHABO5.jpg'
        body['body']['contents'][0]['text'] = '請選擇美食類別'

        body['body']['contents'][2]['contents'][1]['action']['label'] = '火鍋'
        body['body']['contents'][2]['contents'][1]['action']['data'] = 'B&' + self.area + '&火鍋'
        body['body']['contents'][2]['contents'][1]['action']['displayText'] = '火鍋'
        
        body['body']['contents'][2]['contents'][2]['action']['label'] = '早午餐'
        body['body']['contents'][2]['contents'][2]['action']['data'] = 'B&' + self.area + '&早午餐'
        body['body']['contents'][2]['contents'][2]['action']['displayText'] = '早午餐'

        body['body']['contents'][2]['contents'][3]['action']['label'] = '約會餐廳'
        body['body']['contents'][2]['contents'][3]['action']['data'] = 'B&' + self.area + '&約會餐廳'
        body['body']['contents'][2]['contents'][3]['action']['displayText'] = '約會餐廳'

        body['body']['contents'][2]['contents'][4]['action']['label'] = '寵物友善'
        body['body']['contents'][2]['contents'][4]['action']['data'] = 'B&' + self.area + '&寵物友善'
        body['body']['contents'][2]['contents'][4]['action']['displayText'] = '寵物友善'

        return body

# 「選擇消費金額」按鈕樣板訊息
class PriceMessage(Message):
    def __init__(self, category):
        self.category = category
    
    def content(self):
     
        body = json.load(open('food/button.json', 'r', encoding='utf-8'))
        body['hero']['url'] = 'https://i.imgur.com/HBW383b.jpg'
        body['body']['contents'][0]['text'] = '請選擇消費金額'

        body['body']['contents'][2]['contents'][1]['action']['label'] = '150以內'
        body['body']['contents'][2]['contents'][1]['action']['data'] = 'C&' + self.category + '&1'
        body['body']['contents'][2]['contents'][1]['action']['displayText'] = '150以內'
        
        body['body']['contents'][2]['contents'][2]['action']['label'] = '150-600'
        body['body']['contents'][2]['contents'][2]['action']['data'] = 'C&' + self.category + '&2'
        body['body']['contents'][2]['contents'][2]['action']['displayText'] = '150-600'

        body['body']['contents'][2]['contents'][3]['action']['label'] = '600-1200'
        body['body']['contents'][2]['contents'][3]['action']['data'] = 'C&' + self.category + '&3'
        body['body']['contents'][2]['contents'][3]['action']['displayText'] = '600-1200'

        body['body']['contents'][2]['contents'][4]['action']['label'] = '1200以上'
        body['body']['contents'][2]['contents'][4]['action']['data'] = 'C&' + self.category + '&4'
        body['body']['contents'][2]['contents'][4]['action']['displayText'] = '1200以上'

        return body