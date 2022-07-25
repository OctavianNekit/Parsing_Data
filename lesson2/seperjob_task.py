from bs4 import BeautifulSoup as bs
import requests as req
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Works_Vacancy']
collections = db.vacancy_collections

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36'}

job = input("Введите интересующую вас вакансию: ")
response = req.get(f'https://russia.superjob.ru/vacancy/search/?keywords={job}', headers=headers)
value = 0
page = 2
k = 0
source = 'https://russia.superjob.ru/'
while True:
    dom = bs(response.text, 'html.parser')
    job_list = dom.find_all('div', {'class': ['iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL']})
    for job in job_list:
        data = job.find('a')
        name = data.getText()
        link = source + data['href']
        value += 1
        profit = job.find('span', {'class': ['_3mfro _2Wp8I PlM3e _2JVkc _2VHxz']}).getText()
        min_profit = None
        max_profit = None
        currency = None
        if profit == 'По договорённости':
            pass
        else:
            profit_list = profit.split("\xa0")
            currency = profit_list[-1]
            if '—' in profit_list:
                min_profit = int(profit_list[0] + profit_list[1])
                max_profit = int(profit_list[3] + profit_list[4])
            elif 'от' in profit_list:
                min_profit = int(profit_list[1] + profit_list[2])
            elif 'до' in profit_list:
                max_profit = int(profit_list[1] + profit_list[2])
        print(f"Вакансия {value}: {name}, зарплата: {profit} ссылка: {link} Источник: {source}")
        document = {'number': value,
                    'name': name,
                    'min_profit': min_profit,
                    'max_profit': max_profit,
                    'currency': currency,
                    'link': link,
                    'source': source}
        if db.job_openings_superjob.find({"$and":
            [
                {"number": {"$eq": value}},
                {"name": {"$eq": name}},
                {"min_profit": {"$eq": min_profit}},
                {"max_profit": {"$eq": max_profit}},
                {"currency": {"$eq": currency}},
                {"link": {"$eq": link}}
            ]}):
            pass
        else:
            db.job_openings_hh.insert_one(document)
            k += 1
        db.job_openings_superjob.insert_one(document)
    if dom.find('a', {'rel': 'next'}):
        response = req.get(f"https://russia.superjob.ru/vacancy/search/?keywords=python&page={page}",
                           headers=headers)
        page += 1
    else:
        break

print(f"Выведено {value} вакансий")
print(f"Добавлено {k} новых вакансий")
