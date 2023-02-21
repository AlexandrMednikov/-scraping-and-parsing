from bs4 import BeautifulSoup as bs
import lxml
import requests
import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
vacancy = config['Vacancy for parse']['vacancy']
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.934 Yowser/2.5 Safari/537.36'}
hrefs = []
titles = []
wages_min = []
wages_max = []
currency = []
source = []

try:
    for page in range(40):
        url = f"https://nn.hh.ru/search/vacancy?text={vacancy}&page={page}"
        response = requests.get(url, headers=headers)
        dom = bs(response.text, 'lxml')
        list_of_blocks_with_vacancies = dom.find_all('div', {'class':'vacancy-serp-item-body__main-info'})

        for element in list_of_blocks_with_vacancies:
            hrefs.append(element.find('a', {'class':'serp-item__title'})['href'])
            titles.append(element.find('a', {'class': 'serp-item__title'}).text)
            salary = element.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            #заполнение полей мин.зп, макс.зп, валюта
            if salary:
                salary = salary.text.replace("\u202f", "").replace("\xa0", "").split(' ')
                if salary[0] == "от":
                    wages_min.append(int(salary[1]))
                    wages_max.append(0)
                    currency.append(salary[2])
                elif salary[0] == "до":
                    wages_min.append(0)
                    wages_max.append(int(salary[1]))
                    currency.append(salary[2])
                else:
                    wages_min.append(int(salary[0]))
                    wages_max.append(int(salary[2]))
                    currency.append(salary[3])
            else:
                wages_min.append(0)
                wages_max.append(0)
                currency.append(0)

            source.append("hh")
except:
    pass
finally:
    data = {"Title": titles, "Wage min": wages_min, "Wage max": wages_max, "Currency": currency, "Link": hrefs, "Source": source}
    df = pd.DataFrame(data)
    df.astype({"Wage min": "int64", "Wage max": "int64"})
    df.to_csv("result.csv")