import requests
from stock import Stock_Machine
from news import NewsRelated
from data import companies


class StockView:
    def __init__(self, num, alp_key, news_api):
        self.companies = companies
        self.SYMBOL = companies[num]["symbol"]
        self.COMPANY_NAME = companies[num]["name"]

        self.my_stock = Stock_Machine(self.SYMBOL, alp_key)
        self.my_news = NewsRelated(self.COMPANY_NAME,
                                   day1=self.my_stock.day_list[1],
                                   day2=self.my_stock.day_list[0],
                                   api_key=news_api)

    def get_percentage(self):
        messages = []
        percentage = self.my_stock.percentage
        if -1 >= percentage or percentage >= 1:
            # news_data = self.news()
            if percentage >= 1:
                messages += [f"{self.COMPANY_NAME}: 🔺{percentage}%"]
            elif percentage <= -1:
                messages += [f"{self.COMPANY_NAME}: 🔻{percentage}%"]

            messages += [f"Headline: {self.my_news.final_data[0]['title']}\n{self.my_news.final_data[0]['url']}\n"]
            messages += [f"Headline: {self.my_news.final_data[1]['title']}\n{self.my_news.final_data[1]['url']}\n"]
            messages += [f"Headline: {self.my_news.final_data[2]['title']}\n{self.my_news.final_data[2]['url']}\n"]

        else:
            messages += [f"{self.COMPANY_NAME} hasn't seen more than 1% of changes."]
        return messages
