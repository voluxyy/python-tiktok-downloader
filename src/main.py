import requests
import re
import os
import json
import tkinter as tk

global apiKey
with open(".token", "+r") as f:
    apiKey = f.readline()

def interface():
    window = tk.Tk()

    frame = tk.Frame(master=window, width=300, height=100)

    label = tk.Label(text="Nombre de vidéo à télécharger: ", master=frame)
    label.place(x=0, y=0)

    text = tk.Entry(master=frame)
    text.place(x=0, y=25)

    def buttonPressed():
        try:
            nbr = text.get()
            if not nbr.isdigit():
                raise Exception()
        except:
            label2 = tk.Label(text="Il faut entre un nombre.", master=frame)
            label2.place(x=0, y=75)

            frame.pack()
            return
        
        process()

    button = tk.Button(master=frame,
                       text="Download",
                       bg="gray",
                       fg="white",
                       command=buttonPressed
                       )
    button.place(x=0, y=50)
    
    frame.pack()
    window.mainloop()


def terminal():
    while True:
        link = input("Link: ")
        linkRegex = re.compile(r'^https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+$')
        if linkRegex.match(link):
            break
        
        print("Bad link")

    resp = getVideoByUrl(link)

    if resp['reponseJson']['success']:
        print("Request success")
        downloadUrl(resp['reponseJson']['url_list'])
    else:
        print(f"Request failed: {resp['response'].status_code}")


def process():
    users = openConfig()

    data = []
    dataUserInfo = openJson("usersInfos.json")
    dataVideos = openJson("videos.json")
    for index, user in users:
        #userInfo = getUserInfos(user['name'])['user_list'][0]['user']
        #videos = getUserVideos(userInfo)['videos']

        userInfo = dataUserInfo[index]
        videos = dataVideos[index]

        for video in videos:
            data.append({
                'user': {
                    'id': userInfo['id'],
                    'uniqueId': userInfo['uniqueId'],
                    'secUid': userInfo['secUid']
                },
                'videos': video,
            })

    urlList = []
    for info in data:
        print(info['videos'])
        urlList.append(f"https://www.tiktok.com/@{info['user']['uniqueId']}/video/{info['videos']['video_id']}")

    #for url in urlList:
    #    getVideoByUrl(url)

    downloadUrl(urlList)


def saveData(file_path, data):
        try:
            with open(file_path, "+w") as f:
                json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"An error has been encountered while trying to save in json file. This is the error: {error.args[1]}")


def openJson(file_path) -> []:
        try:
            with open(file_path, '+r') as f:
                existing_data = json.load(f)
        except Exception as error:
            print(f"An error has been encountered while trying to open json file. This is the error: {error.args[1]}")
            existing_data = []
            
        return existing_data


def openConfig() -> []:
    try:
        with open("users.json") as f:
            users = json.load(f)
    except Exception as e:
        return e

    return users


def getUserInfos(username):
    url = "https://tiktok-download-video1.p.rapidapi.com/searchUser"

    querystring = {"keywords": username, "count": "1", "cursor": "0"}

    headers = {
    	"X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok-download-video1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['data']


def getUserVideos(user):
    url = "https://tiktok-download-video1.p.rapidapi.com/userPublishVideo"

    querystring = {"unique_id": user['uniqueId'], "user_id": user['id'], "count": "1", "cursor": "0"}

    headers = {
    	"X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok-download-video1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['data']


def getVideoByUrl(link):
    apiUrl = "https://tiktok82.p.rapidapi.com/getDownloadVideo"

    params = {"video_url": str(link)}
    
    headers = {
    	"X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok82.p.rapidapi.com"
    }

    response = requests.get(apiUrl, headers=headers, params=params)
    reponseJson = response.json()

    if reponseJson['success']:
        print("Request success")
        downloadUrl(reponseJson['url_list'])
    else:
        print(f"Request failed: {response.status_code}")


def downloadUrl(urlList):
    noOne = False
    for url in urlList:
        data = requests.get(url)
        if data.status_code == 200:
            noOne = True
            break

    if not noOne:
        print("Links to download aren't working")
        exit(1)

    file = "video"
    i = 0
    ext = ".mp4"

    while True:
        if os.path.exists(f"{file}{i}{ext}"):
            i += 1
        else:
            break

    with open(f"{file}{i}{ext}", "+wb") as f:
        f.write(data.content)
        print(f"Video downloaded with name: {file}{i}{ext}")


if __name__ == "__main__":
    interface()