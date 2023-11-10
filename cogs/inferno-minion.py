import discord, json, traceback
from discord import app_commands
from discord.ext import commands


class InfernoMinion(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "inferno-minion",
        description="This will list all inferno minion stuff"
    )

    async def InfernoMinion(self, interaction: discord.Interaction) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866,      #Ray
                419714628059267072,     #Chiaki
                379823217361027082
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            try:
                bazaar_items = self.bot.hypixel_api.bazaar
                wanted = [
                    "VERY_CRUDE_GABAGOOL",
                    "CRUDE_GABAGOOL_DISTILLATE",
                    "CRUDE_GABAGOOL",
                    "FUEL_GABAGOOL",
                    "HEAVY_GABAGOOL",
                    "HYPERGOLIC_GABAGOOL",
                    "SULPHURIC_COAL",
                    "ENCHANTED_SULPHUR",
                    "ENCHANTED_COAL"
                ]
                items = {i:bazaar_items[i]["quick_status"] for i in wanted}
                sulphuric_coal_price = (items["ENCHANTED_COAL"]["buyPrice"] * 16 + items["ENCHANTED_SULPHUR"]["buyPrice"])/4
                fuel_gabagool_profit_per = (items["FUEL_GABAGOOL"]["buyPrice"] - sulphuric_coal_price)/(24)
                heavy_gabagool_profit_per = (items["HEAVY_GABAGOOL"]["buyPrice"] - sulphuric_coal_price*24)/(24*24)
                hypergolic_gabagool_profit_per = (items["HYPERGOLIC_GABAGOOL"]["buyPrice"] - sulphuric_coal_price*24*24)/(24*24*12)
                very_crude_profit_per = (items["VERY_CRUDE_GABAGOOL"]["buyPrice"])/(24*8)
                lowest = min([items["CRUDE_GABAGOOL"]["buyPrice"], very_crude_profit_per, fuel_gabagool_profit_per, heavy_gabagool_profit_per, hypergolic_gabagool_profit_per])
                best_crude =  max([items["CRUDE_GABAGOOL"]["buyPrice"], very_crude_profit_per, fuel_gabagool_profit_per, heavy_gabagool_profit_per, hypergolic_gabagool_profit_per])
                fuel_cost = items["CRUDE_GABAGOOL_DISTILLATE"]["sellPrice"] * 180 + (best_crude * 6912 * 30 + sulphuric_coal_price * 2 ) + lowest * 24 * 60
                crudes_needed = fuel_cost/best_crude
                await interaction.response.send_message(f"""```
CRUDE_GABAGOOL: {int(items['CRUDE_GABAGOOL']['buyPrice']):,d}
VERY_CRUDE_GABAGOOL: {int(very_crude_profit_per):,d}
FUEL_GABAGOOL: {int(fuel_gabagool_profit_per):,d}
HEAVY_GABAGOOL: {int(heavy_gabagool_profit_per):,d}
HYPERGOLIC_GABAGOOL: {int(hypergolic_gabagool_profit_per):,d}
FUEL_COST: {int(fuel_cost):,d}
CRUDE_GABAGOOL_NEEDED_TO_PROFIT: {int(crudes_needed):,d}
```""", ephemeral=True)

            except Exception as e:
                print(traceback.format_exc())                
                await interaction.response.send_message(f"An error has occured please report this to a developer\n```py{e}```", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(e,ephemeral=True)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        InfernoMinion(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )