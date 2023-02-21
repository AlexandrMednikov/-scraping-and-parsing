from configparser import ConfigParser
from pymongo import MongoClient

# кофниг
config = ConfigParser()
config.read('config.ini')
adress = config['MongoDB key']['key']

# монго
client = MongoClient(adress)
db = client.vacancy


# функции для запросов

def get_vacancy_for_min(min):
    """
    
    :param min: минимальная зп
    :return: вакансии с указанным минимум по зп
    """
    return db.hh.find({"Wage min": {"$gte": min}})

# запросы
for i in get_vacancy_for_min(85000):
    print(i)
