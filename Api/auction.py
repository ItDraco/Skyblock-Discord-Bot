import httpx
import concurrent.futures

def GetPage(url):
    try:
        with httpx.Client() as client:
            response = client.get(url)
            if response.status_code == 200:
                data = response.json()
                items = []
                for item in data["auctions"]:
                    if item.get("bin"):
                        items.append({
                            "item_name": item.get("item_name"),
                            "price": item.get("starting_bid"),
                            "item_lore": item.get("item_lore"),
                            "tier": item.get("tier"),
                            "item_bytes": item.get("item_bytes"),
                            "auctioneer": item.get("auctioneer"),
                            "uuid": item.get("uuid")
                        })
                return items
            else:
                return []
    except Exception as e:
        print(f"Error fetching page: {url}\n{e}")
        return []


def GetAuctions():
    response = httpx.get("https://api.hypixel.net/skyblock/auctions?page=0")
    if response.status_code == 200:
        data = response.json()
        urls = [f"https://api.hypixel.net/skyblock/auctions?page={i}" for i in range(0, data["totalPages"])]
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                pages = list(executor.map(GetPage, urls))
            auctions = []
            for page in pages:
                auctions.extend(page)
            return auctions 
        except Exception as e:
            print(e)
            return []
    else:
        print(f"Auctions: {response.status_code}")
        return []