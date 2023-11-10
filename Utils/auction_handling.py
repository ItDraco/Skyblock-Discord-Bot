import re, json, discord, httpx, base64, nbt, io
from DiscordUI.Embeds import Embed
from datetime import datetime
import traceback
def FetchAuctionItems(auctions, local_items):
    for i in local_items:
        i["items_found"] = []

    for auction_item in auctions:
        for local_item in local_items:
            if any(unwanted_name in auction_item["item_name"] for unwanted_name in local_item["unwanted_names"]):
                continue
            if local_item["item_name"] == None:
                pass
            elif local_item["item_name"] not in auction_item["item_name"]:
                continue
            if local_item["tier"] == None:
                pass
            elif auction_item["tier"] != local_item["tier"]:
                continue
            if isinstance(local_item["pet_level"], int):
                pet_level_match = re.search(r'\[Lvl (\d+)\]', auction_item["item_name"])
                if pet_level_match:
                    item_pet_level = int(pet_level_match.group(1))
                    if item_pet_level < local_item["pet_level"]:
                        continue
            if isinstance(local_item["item_lore"]["word_search"], list):
                if any(type(item) != str for item in local_item["item_lore"]["word_search"]):
                    continue
                if any(word not in auction_item["item_lore"] for word in local_item["item_lore"]["word_search"]):
                    continue
            if isinstance(local_item["item_lore"]["unwanted_word_search"], list):
                if any(type(item) != str for item in local_item["item_lore"]["unwanted_word_search"]):
                    continue
                if any(word in auction_item["item_lore"] for word in local_item["item_lore"]["unwanted_word_search"]):
                    continue
            if isinstance(local_item["item_lore"]["attributes"], list):
                if all(isinstance(item,str) for item in local_item["item_lore"]["attributes"]) and len(local_item["item_lore"]["attributes"]) != 0:                
                    if not all(re.search(attr + r"\s+[IVXLCDM]+", auction_item["item_lore"]) for attr in local_item["item_lore"]["attributes"]):
                        continue
                    if local_item["item_name"] == "Attribute Shard" and ("Attack" in auction_item["item_lore"] or "Fishing" in auction_item["item_lore"]):
                        continue
                    auction_item["attributes_found"] = ExtractAttributes(local_item["item_lore"]["attributes"], auction_item["item_lore"])
            if isinstance(local_item["item_lore"]["regex"], str):
                pass # FEATEURE FOR LATER

            if isinstance(local_item["timestamp"], str):
                nbt_data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(auction_item["item_bytes"])))
                timestamp_str = str(nbt_data['i'][0]['tag']['ExtraAttributes']['timestamp'])
                timestamp_date = datetime.strptime(timestamp_str, "%m/%d/%y %I:%M %p")
                #format: "12/07/21 12:00 PM"
                another_date = datetime.strptime(local_item["timestamp"], "%d/%m/%y %I:%M %p")
                if timestamp_date > another_date:
                    continue

            valid_item = auction_item.copy()
            local_item["items_found"].append(valid_item)
    return local_items

def ExtractAttributes(attributes, item_lore):
    roman_dict = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    pattern = "(" + "|".join(attributes) + r")\s+([IVXLCDM]+)"
    attributes_found = re.findall(pattern, item_lore)
    results = []
    for attribute, roman_numeral in attributes_found:
        decimal_value = roman_dict[roman_numeral]
        results.append((attribute, roman_numeral, decimal_value))
    return results

def SortAuctionItems(items):
    for item in items:
        if len(item["item_lore"]["attributes"]) == 0:
            continue
        if len(item["item_lore"]["attributes"]) == 1 and item["item_lore"]["attribute_pricing"]:
            for i in item["items_found"]:
                i["price"] =i["price"]/2**(i["attributes_found"][0][2] -1)
        item["items_found"] = sorted(item["items_found"], key=lambda x: x["price"])
    return items

def ConvertDictToFormatedFile(found_auction_items):
    with open("items/items.txt" ,"w")as f:
        f.write("")
    for item in found_auction_items:
        max_lengths = [len(str(v)) for i in item["items_found"] for v in i.values()]
        if(len(max_lengths)==0):
            continue
        max_length = max(max_lengths)
        with open(f"items/items.txt", "a", encoding="utf-8") as file:
            file.write("="*20+"\n")
            file.write(f'{item["item_name"]}\n')
            file.write("="*20+"\n")
            for i in item["items_found"]:
                line = ""
                for key, value in i.items():
                    if key in ["item_name","price","uuid","attributes_found"]:
                        line += f"{key}: {value}" + " " * (max_length - len(str(value))) + "   |"
                file.write(line + "\n")

async def NotifyAuctionItems(items, client, already_notified):
    guild = client.get_guild(804012489955475527)
    item_ids = []
    for item in items:
        channel = guild.get_channel(item["channel"])
        if item["items_found"]:
            for item_found in item["items_found"]:
                if not item["notify"]:
                    continue
                if item["price_range"]:
                    min_price, max_price = item["price_range"]
                    if not (min_price <= item_found["price"] <= max_price):
                        continue
                description = f"/viewauction `{item_found['uuid']}`\nPrice: `{item_found['price']}`\n"
                if item["item_lore"]["attributes"]:
                    description += f"Attributes: `{str(item_found['attributes_found'])}`\n"
                try:
                    with httpx.Client() as client:
                        if item_found['auctioneer']:
                            response = client.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{item_found['auctioneer']}")
                            if response.status_code == 200:
                                data = response.json()
                                description += f"Auctioneer: `{data['name']}`\n"
                            else:
                                description += "Auctioneer: `Error fetching name`\n"
                except Exception as e:
                    print(f"Error fetching name: {e}")
                    traceback.print_exc()
                    description += "Auctioneer: `Error fetching name`\n"
                item_ids.append(item_found["uuid"])
                if item_found["uuid"] in already_notified:
                    continue
                already_notified.append(item_found["uuid"])
                embed = Embed({"title": item_found['item_name'], "description":description, "color": 0x4169e1}).created_embeds[0]
                message_content = ""                
                for id in item["ids_to_tag"]:
                    message_content += f"<@{id}> "
                await channel.send(message_content, embed=embed)
    return item_ids

async def DeleteNotifiedAuctions(client, notified_auction_ids, current_auction_ids):
    try:
        category = discord.utils.get(client.get_guild(804012489955475527).categories, id=1129008330925416579)
        if category:
            text_channels = [channel.id for channel in category.channels if isinstance(channel, discord.TextChannel)]
            for channel_id in text_channels:
                channel = client.get_channel(channel_id)
                if channel:
                    async for message in channel.history(limit=None):
                        if message.author.id != 856671823873835029:
                            continue
                        match  = re.search(r'\/viewauction `([^`]+)`', message.embeds[0].description)
                        extracted_id = match.group(1)
                        if extracted_id not in current_auction_ids:
                            await message.delete()
                            if extracted_id in notified_auction_ids:
                                notified_auction_ids.remove(extracted_id)
        for id in notified_auction_ids:
            if id not in current_auction_ids:
                notified_auction_ids.remove(id)
    except Exception as e:
        traceback.print_exc()
    
