import requests
import json

userid = input("Введите id пользователя: ")
main_link = requests.get(f"https://api.vk.com/method/account.getProfileInfo?user_ids={userid}&fields=bdate&access_token"
                         f"=ACCESS_TOKEN&v=5"
                         f".130")
main_link2 = requests.get(f"https://api.vk.com/method/friends.get?user_ids={userid}&fields=bdate&access_token"
                          f"=ACCESS_TOKEN&v=5"
                          f".130")
result = [main_link.json(), main_link2.json()]
with open("result.txt", "w") as outfile:
    json.dump(result, outfile)
