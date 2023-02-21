from configparser import ConfigParser
config = ConfigParser()
config['Vacancy for parse'] = {'vacancy': 'junior python'}
config['MongoDB key'] = {'key': 'mongodb://localhost:27017'}
config['headers'] = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.934 Yowser/2.5 Safari/537.36'}

with open('config.ini', 'w') as f:
    config.write(f)