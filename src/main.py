import tkinter as tk
from tkinter import messagebox
import re
import uuid
from Utils.file import File
from Utils.download import Download
from Api.tiktokdownload import Api

def downloadVideos(count):
    users = File.openJson("users.json")

    data = []
    for user in users:
        userInfo = Api.getUserInfos(user['name'])['user_list'][0]['user']
        videos = Api.getUserVideos(userInfo, count)['videos']

        for video in videos:
            if video['is_top'] == 0:
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
        urlList.append(f"https://www.tiktok.com/@{info['user']['uniqueId']}/video/{info['videos']['video_id']}")

    for url in urlList:
        list = Api.getVideoByUrl(url)
        Download.downloadUrl(list)


def usersSettings():
    window = tk.Tk()
    window.title("Users settings")

    users = File.openJson("users.json")

    for user in users:
        tk.Grid()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Tiktok downloader")

    menu = tk.Menu(master=window)
    window.config(menu=menu)   

    optionsMenu = tk.Menu(master=menu)
    optionsMenu.add_command(label="Users", command=usersSettings)
    menu.add_cascade(label="options", menu=optionsMenu)     

    frame = tk.Frame(master=window, width=300, height=200)

    label = tk.Label(text="Nombre de vidéo à télécharger: ", master=frame)
    label.grid(column=0, row=0)

    nbrInput = tk.Entry(master=frame)
    nbrInput.grid(column=0, row=1)

    def buttonNbrPressed():
        try:
            nbr = nbrInput.get()
            if not nbr.isdigit():
                raise Exception()
        except:
            nbrErrorLabel = tk.Label(text="Il faut entre un nombre.", master=frame)
            nbrErrorLabel.grid(column=0, row=3)

            frame.pack()
            return
        
        downloadVideos(nbr)

    button = tk.Button(master=frame,
                       text="Download",
                       bg="gray",
                       fg="white",
                       command=buttonNbrPressed
                       )
    button.grid(column=0, row=2)

    label2 = tk.Label(text="Lien de la vidéo à télécharger: ", master=frame)
    label2.grid(column=0, row=4)

    linkInput = tk.Entry(master=frame)
    linkInput.grid(column=0, row=5)

    def buttonLinkPressed():
        try:
            link = linkInput.get()
            regex = re.compile(r'^https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+$')
            if not regex.match(link):
                raise Exception()
        except:
            linkErrorLabel = tk.Label(text="Il faut un lien valide.", master=frame)
            linkErrorLabel.grid(column=0, row=7)

            frame.pack()
            return
        
        list = Api.getVideoByUrl(link)
        Download.downloadUrl(list)

    button = tk.Button(master=frame,
                       text="Download from link",
                       bg="gray",
                       fg="white",
                       command=buttonLinkPressed
                       )
    button.grid(column=0, row=6)
    
    frame.pack()
    window.mainloop()