# Задания 1 и 3 добавлены как код в файлы ко второму уроку.
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Works_Vacancy']
collections = db.vacancy_collections

profit = int(input("Введите значения зарплаты: "))

cursor_hh = db.job_openings_hh.find(
    {"$or": [
            {'min_profit': {"$gt": profit}},
            {'max_profit': {"$gt": profit}}
          ]})

cursor_superjob = db.job_openings_superjob.find(
    {"$or": [
            {'min_profit': {"$gt": profit}},
            {'max_profit': {"$gt": profit}}
          ]})

for doc in cursor_hh:
    print(doc)

for doc in cursor_superjob:
    print(doc)
