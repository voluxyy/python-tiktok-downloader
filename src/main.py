import requests
import re
import os
import tkinter as tk

def interface():
    window = tk.Tk()

    frame = tk.Frame(master=window, width=150, height=150)

    label = tk.Label(text="Link: ", master=frame)
    label.place(x=0, y=0)

    text = tk.Entry(master=frame)
    text.place(x=0, y=25)
    
    def buttonPressed():
        link = text.get()
        if not link == "":
            requestApi(link)

    button = tk.Button(master=frame,
                       text="Download",
                       bg="gray",
                       fg="white",
                       command=buttonPressed
                       )
    button.place(x=0, y=100)
    
    frame.pack()

    window.mainloop()

def terminal():
    while True:
        link = input("Link: ")
        linkRegex = re.compile(r'^https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+$')
        if linkRegex.match(link):
            break
        
        print("Bad link")

    resp = requestApi(link)

    if resp['reponseJson']['success']:
        print("Request success")
        downloadUrl(resp['reponseJson']['url_list'])
    else:
        print(f"Request failed: {resp['response'].status_code}")

def requestApi(link):
    apiUrl = "https://tiktok82.p.rapidapi.com/getDownloadVideo"

    params = {"video_url": str(link)}

    with open(".token", "+r") as f:
        apiKey = f.readline()
    
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