import requests

api_url = "https://www.bungie.net/Platform/Destiny2/1/Profile/4611686018456716623/?components=205"
response = requests.get(api_url,headers={"x-api-key":"bc7717e228cd49e58ec26949bba34f51"})
JSON_response = response.json()
print(JSON_response)