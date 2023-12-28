import requests

global apiKey
with open(".token", "+r") as f:
    apiKey = f.readline()

class Api:
    headers = {
        "X-RapidAPI-Key": apiKey,
    	"X-RapidAPI-Host": "tiktok-download-video1.p.rapidapi.com"
    }

    def getUserInfos(username):
        url = "https://tiktok-download-video1.p.rapidapi.com/searchUser"

        querystring = {"keywords": username, "count": "1", "cursor": "0"}

        response = requests.get(url, headers=Api.headers, params=querystring)

        return response.json()['data']


    def getUserVideos(user, count):
        url = "https://tiktok-download-video1.p.rapidapi.com/userPublishVideo"

        querystring = {"unique_id": f"@${user['uniqueId']}", "user_id": user['id'], "count": count, "cursor": "0"}

        response = requests.get(url, headers=Api.headers, params=querystring)

        return response.json()['data']


    def getVideoByUrl(link):
        apiUrl = "https://tiktok-download-video1.p.rapidapi.com/getVideo"
        params = {"url": link, "hd": "1"}

        response = requests.get(apiUrl, headers=Api.headers, params=params)
        responseJson = response.json()

        if responseJson['code'] == 0:
            print("Request success")

            list = []
            list.append(responseJson['data']['play'])
            list.append(responseJson['data']['wmplay'])
            list.append(responseJson['data']['hdplay'])

            return list
        else:
            print(f"Request failed: {response.status_code}")

        return None