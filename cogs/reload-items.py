import discord, json
from discord import app_commands
from discord.ext import commands


class ReloadItems(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "reload-items",
        description="This command will reload the current stored items"
    )

    async def ReloadItems(self, interaction: discord.Interaction) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            try:
                self.bot.item_manager.reload_items()
                await interaction.response.send_message(f"All items have been reloaded", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"An error has occured please report this to a developer\n```py{e}```", ephemeral=True)
            
            
        except Exception as e:
            await interaction.followup.send(e,ephemeral=True)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        ReloadItems(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )