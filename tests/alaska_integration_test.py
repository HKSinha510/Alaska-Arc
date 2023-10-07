#https://github.com/HKSinha510/alaska-integration



import requests, json


try:
    msg =""
    response = requests.get("http://hksinha.webhop.me:8800/systeminfo", timeout=5)
    json_data = json.loads(response.text)
    for key, value in json_data.items():
    	msg += f"{key}: {value}\n"

except Exception as e:
    msg = "Offline "
    print(e)

print(msg)
#response = requests.get("http://hksinha.webhop.me:8800/systeminfo", timeout=5)
print("got response")
json_data = json.loads(response.text)
print(json_data)