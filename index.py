import discord, os, asyncio, json
from discord.ext import commands
import Utils.defaults as defaults
from Utils.item_manager import ItemManager
from Utils.api import HypixelApi

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="-",
            intents=discord.Intents.all(),
            application_id = 856671823873835029
            )
        self.item_manager = None
        self.item_manager = ItemManager(self)

    async def setup_hook(self):
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")

        await client.tree.sync(guild = discord.Object(id= 804012489955475527))

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        await self.wait_until_ready()
        print(f'{self.user} has connected to Discord!')
        while self.item_manager == None:
            pass
        self.hypixel_api = HypixelApi(self)
        asyncio.create_task(self.hypixel_api.update_data())

    async def on_reaction_add(self, reaction, user):
        cat_id = 1129008330925416579
        category = discord.utils.get(self.get_guild(804012489955475527).categories, id=cat_id)
        if category:
            text_channels = [channel.id for channel in category.channels if isinstance(channel, discord.TextChannel)]
            if reaction.message.channel.id in text_channels:
                await reaction.message.delete()
    
client = MyBot()

try:
    client.run(os.environ['BMO_TOKEN'])
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e