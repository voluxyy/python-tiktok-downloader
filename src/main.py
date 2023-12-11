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

# Todo : corriger les erreurs de variable
def process():
    users = openConfig()

    usersInfos = []
    for user in users:
        usersInfos.append(getUserInfos(user['name']))


    videos = []
    for userInfo in userInfo:
        videos.append(getUserVideos(userInfo['user']['id'], userInfo['user']['secUid']))

    urlList = []
    for video in videos:
        urlList.append(f"https://www.tiktok.com/@{video['author']['uniqueId']}/video/{video['id']}")

    downloadUrl(urlList)


def openConfig() -> []:
    try:
        with open("users.json") as f:
            users = json.load(f)
    except Exception as e:
        return e

    return users


def getUserInfos(username):
    url = "https://tiktok82.p.rapidapi.com/getProfile"

    querystring = {"username": username}

    headers = {
    	"X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok82.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def getUserVideos(userId, userSecUid):
    url = "https://tiktok82.p.rapidapi.com/getUserVideos"

    querystring = {"user_id": userId,"secUid": userSecUid}

    headers = {
    	"X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok82.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['items']


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