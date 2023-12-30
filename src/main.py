import tkinter as tk
import re
from utils.file import File
from utils.download import Download
from api.tiktokdownload import TiktokDownload
from api.tiktok import Tiktok

global userFile
userFile = File("users.json")

def downloadVideos(count):
    users = userFile.open()

    data = []
    for user in users:
        userInfo = TiktokDownload().getUserInfos(user['name'])['user_list'][0]['user']
        videos = TiktokDownload().getUserVideos(userInfo, count)['videos']

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
        list = TiktokDownload().getVideoByUrl(url)
        Download(list)


def removeUser(id):
    print(id)


def usersSettings():
    window = tk.Tk()
    window.title("Users settings")

    users = userFile.open()

    title = tk.Label(master=window, text="Users: ")
    title.grid(column=0, row=0)

    frame = tk.Frame(master=window)
    frame.grid(column=0, row=1)

    for i, user in enumerate(users):
        userName = tk.Label(master=frame, text=user['name'])
        userName.grid(column=0, row=i)

        cross = tk.Button(master=frame, text="x")
        cross.grid(column=1, row=i)


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
            nbrErrorLabel = tk.Label(text="Il faut entre un nombre.", master=frame, fg="red")
            nbrErrorLabel.grid(column=0, row=3)

            frame.pack()
            return
        
        downloadVideos(nbr)

    button = tk.Button(master=frame,
                       text="Download",
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
            linkErrorLabel = tk.Label(text="Il faut un lien valide.", master=frame, fg="red")
            linkErrorLabel.grid(column=0, row=7)

            frame.pack()
            return
        
        list = TiktokDownload().getVideoByUrl(link)
        Download(list)

    button = tk.Button(master=frame,
                       text="Download from link",
                       command=buttonLinkPressed
                       )
    button.grid(column=0, row=6)
    
    frame.pack()
    window.mainloop()