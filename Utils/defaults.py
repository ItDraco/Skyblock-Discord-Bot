import aiofiles, json, asyncio

def GetJsonFile(file_path) ->dict:
  with open(file_path,"r") as f:
    return json.load(f)

def WriteJsonFile(file_path, data) ->None:
  with open(file_path, 'w') as outfile:
    json.dump(data, outfile, indent=4)

def GetStoredItems():
  return GetJsonFile("./jsons/items.json")

def WriteStoredItems(data:dict):
  WriteJsonFile("./jsons/items.json", data=data)

async def DeleteAllMessages(client, channel):
    channel = client.get_channel(channel)
    async for message in channel.history(limit=None):
      if message.author.id == await client.user.id:
        await message.delete()
        await asyncio.sleep(1)

async def DeleteMessage(message,seconds):
  await asyncio.sleep(seconds)
  await message.delete()
