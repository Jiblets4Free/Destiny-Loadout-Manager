import requests, zipfile, os, pickle, json, sqlite3

def get_manifest():
    manifest_url = 'http://www.bungie.net/Platform/Destiny/Manifest/'

    #get the manifest location from the json
    r = requests.get(manifest_url,headers={"x-api-key":"bc7717e228cd49e58ec26949bba34f51"})
    manifest = r.json()
    mani_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']

    #Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    #Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], 'Manifest.content')
    print('Unzipped!')

hashes = {
    'DestinyActivityDefinition': 'activityHash',
    'DestinyActivityTypeDefinition': 'activityTypeHash',
    'DestinyClassDefinition': 'classHash',
    'DestinyGenderDefinition': 'genderHash',
    'DestinyInventoryBucketDefinition': 'bucketHash',
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyProgressionDefinition': 'progressionHash',
    'DestinyRaceDefinition': 'raceHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyUnlockFlagDefinition': 'flagHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyDirectorBookDefinition': 'bookHash',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyDestinationDefinition': 'destinationHash',
    'DestinyPlaceDefinition': 'placeHash',
    'DestinyActivityBundleDefinition': 'bundleHash',
    'DestinyStatGroupDefinition': 'statGroupHash',
    'DestinySpecialEventDefinition': 'eventHash',
    'DestinyFactionDefinition': 'factionHash',
    'DestinyVendorCategoryDefinition': 'categoryHash',
    'DestinyEnemyRaceDefinition': 'raceHash',
    'DestinyScriptedSkullDefinition': 'skullHash',
    'DestinyGrimoireCardDefinition': 'cardId'
}

def build_dict(hash_dict):
    #connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    #create a cursor object
    cur = con.cursor()

    all_data = {}
    #for every table name in the dictionary
    for table_name in hash_dict.keys():
        #get a list of all the jsons from the table
        cur.execute('SELECT json from '+table_name)
        print('Generating '+table_name+' dictionary....')

        #this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        #create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        #create a dictionary with the hashes as keys
        #and the jsons as values
        item_dict = {}
        hash = hash_dict[table_name]
        for item in item_jsons:
            item_dict[item[hash]] = item

        #add that dictionary to our all_data using the name of the table
        #as a key.
        all_data[table_name] = item_dict

    print('Dictionary Generated!')
    return all_data

def get_profile(ProdifileID,CharacterID):
    api_url = "https://www.bungie.net/Platform/Destiny2/2/Profile/" + str(ProdifileID) + "/?components=205" #This URL is specific to my account currently (Acer, Topper of Laps)
    response = requests.get(api_url,headers={"x-api-key":"bc7717e228cd49e58ec26949bba34f51"}) #This requests the above URL and adds the api key into the header so that the Destiny API doesnt reject the request
    JSON_response = response.json()
    myItems = JSON_response["Response"]["characterEquipment"]["data"][CharacterID]["items"]
    for item in myItems:
        print(get_item_info(item["itemHash"])[0] + " | " + get_item_info(item["itemHash"])[1] + " | " + get_item_info(item["itemHash"])[2])

def get_item_info(hash):
    try: #This tries to Convert the hash into an item List
        item = all_data['DestinyInventoryItemDefinition'][int(hash)]
        return[item['itemName'],item['itemTypeName'],item['tierTypeName']]
    except KeyError:
        return(["Could","Not","Load - KeyError hash = " + str(hash)])

if __name__ == "__main__":
    #check if pickle exists, if not create one.
    if os.path.isfile(r'manifest.content') == False:
        get_manifest()
        all_data = build_dict(hashes)
        with open('manifest.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest.pickle' created!\nDONE!")
    else:
        print('Pickle Exists')

    with open('manifest.pickle', 'rb') as data:
        all_data = pickle.load(data)

    get_profile("4611686018513964725","2305843010086124237")

#566976653 - not working
#1274330687 - ghorn
