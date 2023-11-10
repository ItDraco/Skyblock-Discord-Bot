import discord,json
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
        self.item_manager.remove_item(self.item_type, self.new_item)
        await interaction.response.send_message("This item has been removed", ephemeral=True)

class RemoveItem(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    @app_commands.command(
        name = "remove-item",
        description="This command will reload all commands"
    )
    @app_commands.choices(
        item_type=[
            app_commands.Choice(name="Auctions", value="auctions"),
            app_commands.Choice(name="Bazaar", value="bazaar")
        ]
    )

    async def RemoveItem(self, interaction: discord.Interaction, item_type:str, item_number:int) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            items = self.bot.item_manager.get_items(item_type)
            if 0 <= item_number-1 < len(items):
                await interaction.response.send_message(f"Are you sure you want to delete\n ```{json.dumps(items[item_number-1])}```",view=New_View(items=[ConfirmItem(self.bot.item_manager, item_type, items[item_number-1])]),ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        RemoveItem(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )