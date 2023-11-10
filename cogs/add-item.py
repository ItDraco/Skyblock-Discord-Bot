import discord, json
from DiscordUI.Views import New_View
from discord.ui import Button
from discord import app_commands
from discord.ext import commands

class ConfirmItem(Button):
    def __init__(self, item_manager, item_type, new_item):
        super().__init__(style=discord.ButtonStyle.green, label="Confirm")
        self.item_manager = item_manager
        self.item_type = item_type
        self.new_item = new_item

    async def callback(self, interaction):
        self.item_manager.add_item(self.item_type, self.new_item)
        await interaction.response.send_message("This item has been added", ephemeral=True)

class AddItem(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "add-item",
        description="This command will add new items to be checked in the auction house"
    )
    @app_commands.choices(
        item_type=[
            app_commands.Choice(name="Auctions", value="auctions"),
            app_commands.Choice(name="Bazaar", value="bazaar")
        ]
    )

    async def AddItem(self, interaction: discord.Interaction, item_type:str, item_name: str, channel:discord.TextChannel = None, notifiable:bool = None, price_range:str = None, attributes:str = None) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            new_item = {
                    "item_name": item_name,
                    "attributes": [str(price) for price in attributes.split(",")] if attributes else [],
                    "channel": channel.id if channel else 1129008673277091880,
                    "notify": {
                            "allow":notifiable if notifiable else False,
                            "price_range": [int(price) for price in price_range.split(",")] if price_range else []
                        },
                    "banned_items":[]
                }
            await interaction.response.send_message(f"Are you sure you want to add:\n ```{json.dumps(new_item,indent=4)}```",view=New_View(items=[ConfirmItem(self.bot.item_manager,item_type, new_item)]), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e,ephemeral=True)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        AddItem(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )