import discord, json
from discord import app_commands
from discord.ext import commands


class ShowItems(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "show-items",
        description="This command will show the current stored items"
    )

    async def ShowItems(self, interaction: discord.Interaction) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            await interaction.response.send_message(f"auctions items:\n", ephemeral=True)
            auction_items = self.bot.item_manager.get_items("auctions")
            message_content = ""
            for index, item in enumerate(auction_items):
                # print(index)
                # print(json.dumps(item, indent=4))
                
                line = f'{index}. {item["item_name"]}, '
                if item["attributes"]:
                    line += f'{item["attributes"]}, '
                if item["notify"]["allow"]:
                    line += "Will notify, "
                if item["notify"]["price_range"]:
                    line += (" -> ".join([str(i) for i in item["notify"]["price_range"]]))
                line+="\n"

                if len(message_content)+len(line) > 2000:
                    await interaction.followup.send(message_content, ephemeral=True)
                    message_content = ""
                    continue
                message_content += line
            await interaction.followup.send(message_content, ephemeral=True)

            #await interaction.response.send_message(file=discord.File("./jsons/items.json"))
        except Exception as e:
            await interaction.followup.send(e,ephemeral=True)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        ShowItems(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )