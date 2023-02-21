from bs4 import BeautifulSoup as bs
import lxml
import requests
from configparser import ConfigParser
from pymongo import MongoClient

# конфиг
config = ConfigParser()
config.read('config.ini')
adress = config['MongoDB key']['key']
vacancy = config['Vacancy for parse']['vacancy']
user_agent = config['headers']['user-agent']

# монго
client = MongoClient(adress)
db = client.vacancy

# далее только парсер
try:
    for page in range(40):
        url = f"https://nn.hh.ru/search/vacancy?text={vacancy}&page={page}"
        response = requests.get(url, headers={'user-agent': user_agent})
        dom = bs(response.text, 'lxml')
        list_of_blocks_with_vacancies = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})

        for element in list_of_blocks_with_vacancies:
            hrefs = element.find('a', {'class': 'serp-item__title'})['href']
            titles = element.find('a', {'class': 'serp-item__title'}).text
            salary = element.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            # заполнение полей мин.зп, макс.зп, валюта
            if salary:
                salary = salary.text.replace("\u202f", "").replace("\xa0", "").split(' ')
                if salary[0] == "от":
                    wages_min = int(salary[1])
                    wages_max = 0
                    currency = salary[2]
                elif salary[0] == "до":
                    wages_min = 0
                    wages_max = int(salary[1])
                    currency = salary[2]
                else:
                    wages_min = int(salary[0])
                    wages_max = int(salary[2])
                    currency = salary[3]
            else:
                wages_min = 0
                wages_max = 0
                currency = 0

            source = 'hh'

            data = {"Title": titles, "Wage min": wages_min, "Wage max": wages_max, "Currency": currency, "Link": hrefs,
                    "Source": source}

            #для отсутствия дублей
            got = 0
            for item in db.hh.find():
                if item['Link'] == hrefs:
                    got += 1

            if not got:
                db.hh.insert_one(data)
except:
    pass
