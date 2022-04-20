from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

# 美食抽象類別
class Food(ABC):

    def __init__(self, area):
        self.area = area # 地區

    @abstractmethod
    def scrape(self):
        pass

# 愛食記爬蟲
class IFoodie(Food):
    
    def scrape(self):
        response = requests.get("https://ifoodie.tw/explore/" + self.area + "/list?sortby=popular&opening=true")
        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-558691085 restaurant-info'}, limit=5)

        content = ""
        for card in cards:

            title = card.find(
                "a", {"class": "jsx-558691085 title-text"}).getText()
            
            rating = card.find(
                "div", {"class": "jsx-1207467136 text"}).getText()
            
            address = card.find(
                "div", {"class": "jsx-558691085 address-row"}).getText()
            
            url = 'https://ifoodie.tw/' + card.find(
                "a", {"class": "jsx-558691085 title-text"})['href']

            content += f"{title} \n{rating}顆星 \n{address} \n{url} \n\n"
        
        return content