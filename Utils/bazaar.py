import requests

def FetchBazaarItems(bazaar_items, wanted_items):
    notify_items = []
    found_items = []
    for item in wanted_items:
        if bazaar_items[item["item_name"]]["quick_status"]["buy_price"] < item["wanted_price"]:
            notify_items.append(item)
        found_items.append(item)
    return found_items, notify_items
        

    

def NotifyBazaarItems(found_items, client, notified_bazaar):
    pass