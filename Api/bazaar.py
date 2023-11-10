import requests

def GetBazaar():
    try:
        response = requests.get("https://api.hypixel.net/skyblock/bazaar")
        if response.status_code == 200:
            data = response.json()
            return data["products"]
        else:
            return []
    except Exception as e:
        print(f"Error fetching bazaar\n{e}")
        print(response.status_code)
        print(response.content)
        return []