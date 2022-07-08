import requests

if __name__ == "__main__":
    print("Must run main.py")

def getToken(email, password):
    headers = {
        "authority": "ebook.pazdro.com.pl",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "iCraze",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://ebook.pazdro.com.pl",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://ebook.pazdro.com.pl/auth/login",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8"
    }

    req = requests.post("https://ebook.pazdro.com.pl/api/auth/login", headers=headers, json={
        "username": email,
        "password": password,
        "roles": ["user"]
    })

    response = req.json()

    if "statusCode" in response:
        return {"error": True, "message": f"Error fetching access token ({response['message']})"}
    else:
        return {"error": False, "message": response["accessToken"]}