import re
from utils.gui import Gui
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
    window = gui.Window()
    window.title("Users settings")

    users = userFile.open()

    gui.Label(master=window, text="Users: ", column=0, row=0)

    frame = gui.Frame(master=window, column=0, row=1)

    for i, user in enumerate(users):
        gui.Label(master=frame, text=user['name'], column=0, row=i)

        gui.Button(master=frame, text="x", command=lambda: removeUser(user['id']), column=1, row=i)


if __name__ =="__main__":
    gui = Gui()

    window = gui.Window()
    window.title("Tiktok downloader")

    menu = gui.Menu(master=window)
    window.config(menu=menu)

    optionsMenu = gui.Menu(master=menu)
    optionsMenu.add_command(label="Users", command=usersSettings)
    menu.add_cascade(label="Options", menu=optionsMenu)

    frame = gui.Frame(master=window, column=0, row=0)

    label = gui.Label(master=frame, text="Nombre de vidéo à télécharger: ", column=0, row=0)

    nbrEntry = gui.Entry(master=frame, column=0, row=1)

    def buttonNbrPressed():
        try:
            nbr = nbrEntry.get()
            if not nbr.isdigit():
                raise Exception()
        except:
            gui.Label(master=frame, text="Il faut entre un nombre.", fg="red", column=0, row=3)

            frame.pack()
            return
        
        downloadVideos(nbr)

    nbrButton = gui.Button(master=frame, text="Télécharger", command=buttonNbrPressed, column=0, row=2)

    label2 = gui.Label(master=frame, text="Lien de la vidéo à téléchager: ", column=0, row=4)

    linkEntry = gui.Entry(master=frame, column=0, row=5)

    def buttonLinkPressed():
        try:
            link = linkEntry.get()
            regex = re.compile(r'^https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+$')
            if not regex.match(link):
                raise Exception()
        except:
            gui.Label(master=frame, text="Il faut un lien valide.", fg="red", column=0, row=7)

            frame.pack()
            return
        
        list = TiktokDownload().getVideoByUrl(link)
        Download(list)

    linkButton = gui.Button(master=frame, text="Télécharger", command=buttonLinkPressed, column=0, row=6)

    window.mainloop()
