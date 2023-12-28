import tkinter as tk
import re
from Utils.file import File
from Utils.download import Download
from Api.tiktokdownload import Api

def interface():
    window = tk.Tk()

    frame = tk.Frame(master=window, width=300, height=200)

    label = tk.Label(text="Nombre de vidéo à télécharger: ", master=frame)
    label.place(x=0, y=0)

    nbrInput = tk.Entry(master=frame)
    nbrInput.place(x=0, y=25)

    def buttonNbrPressed():
        try:
            nbr = nbrInput.get()
            if not nbr.isdigit():
                raise Exception()
        except:
            nbrErrorLabel = tk.Label(text="Il faut entre un nombre.", master=frame)
            nbrErrorLabel.place(x=0, y=80)

            frame.pack()
            return
        
        downloadVideos(nbr)

    button = tk.Button(master=frame,
                       text="Download",
                       bg="gray",
                       fg="white",
                       command=buttonNbrPressed
                       )
    button.place(x=0, y=50)

    label2 = tk.Label(text="Lien de la vidéo à télécharger: ", master=frame)
    label2.place(x=0, y=100)

    linkInput = tk.Entry(master=frame)
    linkInput.place(x=0, y=125)

    def buttonLinkPressed():
        try:
            link = linkInput.get()
            regex = re.compile(r'^https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+$')
            if not regex.match(link):
                raise Exception()
        except:
            linkErrorLabel = tk.Label(text="Il faut un lien valide.", master=frame)
            linkErrorLabel.place(x=0, y=180)

            frame.pack()
            return
        
        downloadFromLink(link)


    button = tk.Button(master=frame,
                       text="Download from link",
                       bg="gray",
                       fg="white",
                       command=buttonLinkPressed
                       )
    button.place(x=0, y=150)
    
    frame.pack()
    window.mainloop()


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


def downloadFromLink(link):
    list = Api.getVideoByUrl(link)
    Download.downloadUrl(list)


if __name__ == "__main__":
    interface()