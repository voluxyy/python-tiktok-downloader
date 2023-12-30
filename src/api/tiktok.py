import requests

class Tiktok:
    def __init__(self) -> None:
        """Init a tiktok instance."""

        with open(".token", "+r") as f:
            key = f.readline()

        self.headers = {
            "X-RapidAPI-Key": key,
    	    "X-RapidAPI-Host": "tiktok82.p.rapidapi.com"
        }


    def getUserInfos(self, username):
        url = "https://tiktok82.p.rapidapi.com/getProfile"

        querystring = {"username": username}

        response = requests.get(url, headers=self.headers, params=querystring)
        responseJson = response.json()

        print(responseJson)

        return None


    def getUserVideos(self, user):
        url = "https://tiktok82.p.rapidapi.com/getUserVideos"

        querystring = {"user_id": user['id'], "secUid": user['secUid']}

        response = requests.get(url, headers=self.headers, params=querystring)
        responseJson = response.json()
        
        print(responseJson)

        return None


    def getVideoByUrl(self, link):
        apiUrl = "https://tiktok82.p.rapidapi.com/getDownloadVideo"
        params = {"video_url": link}

        response = requests.get(apiUrl, headers=self.headers, params=params)
        responseJson = response.json()

        print(responseJson)

        return None