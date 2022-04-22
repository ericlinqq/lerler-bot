from abc import ABC, abstractmethod
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction,
    CarouselColumn,
    MessageTemplateAction,
    URITemplateAction
)

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
        body = TemplateSendMessage(
            alt_text='Buttons template', 
            template=ButtonsTemplate(
                    title='Menu',
                    text='請選擇地區',
                    thumbnail_image_url='https://i.imgur.com/5Ka5gah.jpg',
                    actions=[
                        PostbackTemplateAction(
                            label='台北市',
                            text='台北市',
                            data='A&台北市'
                        ),

                        PostbackTemplateAction(
                            label='台中市',
                            text='台中市',
                            data='A&台中市'
                        ),

                        PostbackTemplateAction(
                            label='台南市',
                            text='台南市',
                            data='A&台南市'
                        ),

                        PostbackTemplateAction(
                            label='高雄市',
                            text='高雄市',
                            data='A&高雄市'
                        )
                    ]
                )
            )
        return body

# 「選擇美食類別」按鈕樣板訊息
class CategoryMessage(Message):
    def __init__(self, area):
        self.area = area
    
    def content(self):
        body = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                    title='Menu',
                    text='請選擇美食類別',
                    thumbnail_image_url='https://i.imgur.com/8XHABO5.jpg',
                    actions=[
                        PostbackTemplateAction(
                            label='火鍋',
                            text='火鍋',
                            data='B&' + self.area +'&火鍋'
                        ),

                        PostbackTemplateAction(
                            label='早午餐',
                            text='早午餐',
                            data='B&' + self.area +'&早午餐'
                        ),

                        PostbackTemplateAction(
                            label='約會餐廳',
                            text='約會餐廳',
                            data='B&' + self.area +'&約會餐廳'
                        )
                    ]
                )
            )
        return body

# 「選擇消費金額」按鈕樣板訊息
class PriceMessage(Message):
    def __init__(self, category):
        self.category = category
    
    def content(self):
        body = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                    title='Menu',
                    text='請選擇消費金額',
                    thumbnail_image_url='https://i.imgur.com/HBW383b.jpg',
                    actions=[
                        PostbackTemplateAction(
                            label='150以內',
                            text='150以內',
                            data='C&' + self.category +'&1'
                        ),

                        PostbackTemplateAction(
                            label='150-600',
                            text='150-600',
                            data='C&' + self.category +'&2'
                        ),

                        PostbackTemplateAction(
                            label='600-1200',
                            text='600-1200',
                            data='C&' + self.category +'&3'
                        ),

                        PostbackTemplateAction(
                            label='1200以上',
                            text='1200以上',
                            data='C&' + self.category +'&4'
                        )
                    ]
                )
            )
        return body

# 「餐廳」 旋轉樣板訊息
class Restaurant(Message):
    def __init__(self, title, rating, image, address, url):
        self.title = title
        self.rating = rating
        self.image = image
        self.address = address
        self.url = url
    
    def content(self):
        body = CarouselColumn(
            title=self.title,
            text=self.rating + '顆星 \n' + self.address,
            thumbnail_image_url=self.image,
            actions=[
                MessageTemplateAction(
                    label='吃這家',
                    text='我覺得【' + self.title + '】不錯'
                ),
                URITemplateAction(
                    label='在愛食記上瀏覽',
                    uri=self.url
                ),
                URITemplateAction(
                    label='Google Maps',
                    uri='https://www.google.com.tw/maps/place/' + self.address
                )
            ]
        )
        return body