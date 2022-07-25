import requests
import json

username = input('Введите имя пользователя: ')
main_link = requests.get('https://api.github.com/users/'+username+'/repos')
result = {"repo": []}
for repo in range(0, len(main_link.json())):
    result["repo"].append({
        "Номер": repo + 1,
        "Название": main_link.json()[repo]['name'],
        "URL адрес": main_link.json()[repo]['svn_url']
    })
with open('result.txt', 'w') as outfile:
    json.dump(result, outfile)
