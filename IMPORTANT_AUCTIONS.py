import requests,json,re

auctions = [
{
    "uuid": "d6631585d76a41b99a334942f5e94379",
    "auctioneer": "b78e0dcd79f54dd2b234504d3b168cbd",
    "profile_id": "a8558f23e2c947ee8ea5c6099a80946d",
    "coop": [
        "b78e0dcd79f54dd2b234504d3b168cbd"
    ],
    "start": 1696977697828,
    "end": 1696999297828,
    "item_name": "[Lvl 100] Ammonite",
    "item_lore": "\u00a77Defense: \u00a7a+125\n\u00a77Speed: \u00a7a+15\n\u00a77True Defense: \u00a7a+10\n\u00a77Mining Speed: \u00a7a+10\n \u00a78[\u00a77\u2e15\u00a78] \u00a78[\u00a78\u2618\u00a78]\n\n\u00a76Full Set Bonus: Expert Miner \u00a77(0/4)\n\u00a77Grants \u00a76+2\u2e15 Mining Speed \u00a77for\n\u00a77each of your mining levels.\n\n\u00a77The Defense \u00a77of this item is\n\u00a77doubled while on a mining island\n\n\u00a77\u00a78This item can be reforged!\n\u00a75\u00a7lEPIC LEGGINGS",
    "extra": "Glacite Leggings Leather Leggings",
    "category": "armor",
    "tier": "LEGENDARY",
    "starting_bid": 25000,
    "item_bytes": "H4sIAAAAAAAAAFVRzW7TQBAeJy0k4dBIHHqrpgKhohLq/DgJuZU0NZHSqlLCCSG0tsfOirUd7a6hfRCkvkFegXMepU/BASHGpa2KtNLOfPN938zsNgDq4MgGADgVqMjIeePA9jgvMus0oGpF4sCzj1mgSXwVgSKnCvUPMqJTJRLDoj8NeBpJs1Liqg5bs1xTjdEdeL5ZD04opszQCDdrcdjueNBkcL4iiu4gD3YZWeiC8H+ue1s4k5nMEnyscGGPg+Enrt78/MHR57t0eHN9Xabc/GCz7p8WSuGcLL7Ps8KMcHK5Im2RHUmzYnDgHvVewyuOfC0yaxjrH3bYEh83LZlxrmGPbxLhEvMYr/JCY/qPpOgbKfOWe+6Xeywf1iiFzLVLaVBaSlEaeMFYlBf8hhF+X0pFmGco7q2kUSKL2KmU8iKLB2koMgwINfEkCUX75dN6m7WaXEzHOJv4/vTcn1dhO8wVj1r9/asGW+cipVuer0TILjijJOE2BhqwM7m0Whxbq2VQWDK18teh6c+Ox9PF5Mu9I7sUBRde9t3BgIZe1HIFea1e13Vb77xBt9UOwzgc9uIoCLo1qFuZkrEiXUGz7R7x6XSxP+p6eHEGUIEnJyIVCfGC8Bed0OAucwIAAA==", 
    "claimed": False,
    "claimed_bidders": [],
    "highest_bid_amount": 0,
    "last_updated": 1696977697828,
    "bin": True,
    "bids": [],
    "item_uuid": "6077e85d0ae5430095731ccfc84fdbb3"
}]


auction_wanted = {
    "item_name":"Ammonite",
    "tier":"LEGENDARY",
    "pet_level":100,
    "item_lore":{
        "word_search":None, #["Held Item:","Magma Skin"]
        "attributes":None, #["Veteran","Vitality"],
        "regex":None
    },
    "price_range":[0,500000],
    "timestamp":None,#"12/07/21 12:00 PM"
    "notify":True,
    "channel":1131756584264015952
}
local_items = [auction_wanted]

for auction_item in auctions:
    for local_item in local_items:
        if local_item["item_name"] not in auction_item["item_name"]:
            continue
        if auction_item["tier"]!=local_item["tier"]:
            continue
        if isinstance(local_item["pet_level"], int):
            pet_level_match = re.search(r'\[Lvl (\d+)\]', auction_item["item_name"])
            if pet_level_match:
                item_pet_level = int(pet_level_match.group(1))
                if item_pet_level < local_item["pet_level"]:
                    continue
        if isinstance(local_item["item_lore"]["word_search"], str):
            if local_item["item_lore"]["word_search"] not in auction_item["item_lore"]:
                continue
        if isinstance(local_item["item_lore"]["attributes"], list):
            if all(isinstance(item,str) for item in local_item["item_lore"]["attributes"]):                
                if not all(re.search(attr + r"\s+[IVXLCDM]+", auction_item["item_lore"]) for attr in local_item["item_lore"]["attributes"]):
                    continue
                if local_item["item_name"] == "Attribute Shard" and ("Attack" in auction_item["item_lore"] or "Fishing" in auction_item["item_lore"]):
                    continue
                auction_item["attributes_found"] = ExtractAttributes(item["attributes"], auction_item["item_lore"])
        if isinstance(local_item["item_lore"]["regex"], str):
            pass # FEATEURE FOR LATER

        if isinstance(local_item["timestamp"], str):
            pass # EXTRACT TIMESTAMP AND COMPARE
