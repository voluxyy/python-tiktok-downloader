import requests
import os

class Download:
    def __init__(self, urlList):
        """Init a download instance."""
        self.urls = urlList
        self.downloadUrl()
        

    def downloadUrl(self):
        noOne = False
        for url in self.urls:
            data = requests.get(url)
            if data.status_code == 200:
                noOne = True
                break
            
        if not noOne:
            raise Exception("Links to download aren't working")
    
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