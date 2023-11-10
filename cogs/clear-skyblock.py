import discord
from discord import app_commands
from discord.ext import commands


class ClearSkyblock(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "clear-skyblock",
        description="This command will clear all skyblock channels"
    )

    async def Reload(self, interaction: discord.Interaction) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            cat_id = 1129008330925416579
            category = discord.utils.get(interaction.guild.categories, id=cat_id)
            if category:
                await interaction.response.send_message(f"Now deleting all messages in the category: `{category.name}`", ephemeral=True)
                text_channels = [channel for channel in category.channels if isinstance(channel, discord.TextChannel)]
                
                for channel in text_channels:
                    await channel.purge(limit=None)
            else:
                await interaction.response.send_message("Category not found")
        except Exception as e:
            await interaction.response.send_message(e)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        ClearSkyblock(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )