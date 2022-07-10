import requests

def GetManifest():
    manifest_url = "http://www.bungie.net/Platform/Destiny/Manifest/"
    manifest = requests.get(manifest_url,headers={"x-api-key":"bc7717e228cd49e58ec26949bba34f51"}).json()
    mani_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']
    r = requests.get(mani_url)
    with open("Manifest","wb") as zip:
        zip.write(r.content)
    print("Download complete!")

def GetProfile():
    api_url = "https://www.bungie.net/Platform/Destiny2/1/Profile/4611686018456716623/?components=205" #This URL is specific to my account currently (Acer, Topper of Laps)
    response = requests.get(api_url,headers={"x-api-key":"bc7717e228cd49e58ec26949bba34f51"}) #This requests the above URL and adds the api key into the header so that the Destiny API doesnt reject the request
    JSON_response = response.json()
    myItems = JSON_response["Response"]["characterEquipment"]["data"]["2305843009290026250"]["items"] #The first long number (2305843009294399016) is the character ID for my old titan.
    for item in myItems:
        print(item["itemHash"])

GetManifest()