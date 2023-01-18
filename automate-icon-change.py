import requests, json

# insert secret token from notion integretion
token = ''

# insert database id here
databaseId = ''

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-06-28"
}

switch_icon = {
    "type": "external",
    "external": {
        "url": "https://www.notion.so/icons/swap-horizontally_gray.svg"
    }
}

pc_icon = {
    "type": "emoji",
    "emoji": "💻"
}

ps4_icon = {
    "type": "emoji",
    "emoji": "🎮"
}

def readCurrent(readUrl, headers, json_data=None):

    res = requests.request("POST", readUrl, headers=headers, json=json_data)
    print(res.status_code)
    data = res.json()

    for i in data['results']:
        if i['icon'] != None:
            pass
        elif 'switch' in i['properties']['Status']['select']['name']:
            i['icon'] = switch_icon
        elif 'ps4' in i['properties']['Status']['select']['name']:
            i['icon'] = ps4_icon
        elif 'pc' in i['properties']['Status']['select']['name']:
            i['icon'] = pc_icon
        else:
            print('current game is: ' + i['properties']['Name']['title'][0]['text']['content'])
            pf = str(input("what platform is this under? "))
            if pf == 'sw':
                i['icon'] = switch_icon
            elif pf == 'ps4':
                i['icon'] = ps4_icon
            elif pf == 'pc':
                i['icon'] = pc_icon
    updateAll(data, headers)

    print('updated current 100 pages')

    return res

def readDatabase(databaseId, headers):

    readUrl = f'https://api.notion.com/v1/databases/{databaseId}/query'
    res = requests.request("POST", readUrl, headers=headers)
    print(res.status_code)
    data = res.json()
    readCurrent(readUrl, headers)
    while data['has_more']:
        print('moving onto next 100 items')
        next_curs = data['next_cursor']
        json_data = {'start_cursor': next_curs}
        resp = readCurrent(readUrl, headers, json_data)
        data = resp.json()

    print("all items updated")

def updateAll(update_data, headers):
    for i in update_data['results']:
        pageID = i['id']
        updateUrl = f'https://api.notion.com/v1/pages/{pageID}'
        pageData = {'icon': i['icon']}
        resp = requests.request("PATCH", updateUrl, headers=headers, json=pageData)
        print(resp.status_code)
        print(resp.text)

readUrl = f'https://api.notion.com/v1/databases/{databaseId}/query'
readDatabase(databaseId, headers)