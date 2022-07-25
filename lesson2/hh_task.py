from bs4 import BeautifulSoup as bs
import requests as req
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Works_Vacancy']
collections = db.vacancy_collections

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36'}

job = input("Введите интересующую вас вакансию: ")
response = req.get(
    f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={job}&showClusters=true',
    headers=headers)
value = 0
page = 1
k = 0
source = 'https://hh.ru'
while True:
    dom = bs(response.text, 'html.parser')
    job_list = dom.find_all('div', {'class': ['vacancy-serp-item__row vacancy-serp-item__row_header']})
    for job in job_list:
        data = job.find('a', {'class': 'bloko-link'})
        name = data.getText()
        link = data['href']
        profit = None
        profit_value = job.find('span', {'data-qa': ['vacancy-serp__vacancy-compensation']})
        min_profit = None
        max_profit = None
        currency = None
        if profit_value is not None:
            profit = profit_value.getText()
            profit_list = profit.split(" ")
            profit_list1 = []
            for i in range(len(profit_list)):
                profit_list1.append(profit_list[i].replace('\u202f', ""))
            if profit_list1[0] == "от":
                min_profit = int(profit_list1[1])
                currency = profit_list1[2]
            elif profit_list1[0] == "до":
                max_profit = int(profit_list1[1])
                currency = profit_list1[2]
            else:
                min_profit = int(profit_list1[0])
                max_profit = int(profit_list1[2])
                currency = profit_list1[3]
        value += 1
        print(f"Вакансия {value}: {name}, зарплата {profit} ссылка: {link} Источник: {source}")
        document = {'number': value,
                    'name': name,
                    'min_profit': min_profit,
                    'max_profit': max_profit,
                    'currency': currency,
                    'link': link,
                    'source': source}
        if db.job_openings_hh.find({"$and":
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
    if dom.find('a', {'data-qa': 'pager-next'}):
        response = req.get(f"https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&"
                           f"text=python&showClusters=true&page={page}", headers=headers)
        page += 1
    else:
        break

print(f"Выведено {value} вакансий")
print(f"Добавлено {k} новых вакансий")
