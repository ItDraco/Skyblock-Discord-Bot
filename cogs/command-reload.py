import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class ReloadCommands(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "reload",
        description="This command will reload all commands"
    )

    async def Reload(self, interaction: discord.Interaction, extension: str) -> None:
        ALLOWED_USER_IDS = [296357156926521344]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return

        try:
            await self.bot.unload_extension(f"cogs.{extension}")
            await self.bot.load_extension(f"cogs.{extension}")
            await interaction.response.send_message(f"Command: cogs.{extension} was reloaded", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        ReloadCommands(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )