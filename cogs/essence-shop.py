import discord, json, requests, traceback
from discord import app_commands
from discord.ext import commands

class EssenceShop(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name = "essence-shop",
        description="This command will detail a players essence shops"
    )

    async def EssenceShop(self, interaction: discord.Interaction, username: str,) -> None:
        ALLOWED_USER_IDS = [
                296357156926521344,     #Draco
                482112955547385866      #Ray
            ]
        if interaction.user.id not in ALLOWED_USER_IDS:
            await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
            return
        try:
            response = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}")
            if response.status_code != 200:
                print(response.status_code)
                print(response.reason)
                return
            x = response.json()["profiles"]
            essence_perks = {}
            for profile in x:
                if x[profile]["current"]:
                    essence_perks = x[profile]["data"]["perks"]
                    break
            
            if not essence_perks:
                return
            
            perk_levels = {
                "ESSENCE_UNDEAD":{
                    "catacombs_boss_luck": [100,1000,10000,100000],   
                    "catacombs_looting": [1000,2000,3000,4000,5000],
                    "revive_stone": [200000],
                    "catacombs_health": [1000,2500,5000,10000,25000],      
                    "catacombs_defense": [1000,4000,6000,8000,10000],     
                    "catacombs_intelligence": [1000,4000,6000,8000,10000],
                    "catacombs_strength": [1000,4000,6000,8000,10000],
                    "catacombs_crit_damage": [1000,3000,10000,20000,50000],
                },
                "ESSENCE_WITHER":{
                    "permanent_health": [100,250,500,1000,1500],
                    "permanent_defense": [100,250,500,1000,1500],
                    "permanent_speed": [100,250,500,1000,1500],
                    "permanent_intelligence": [100,250,500,1000,1500],
                    "forbidden_blessing": [200,400,600,800,1000,1200,1400,1600,1800,2000],
                    "permanent_strength": [100,250,500,1000,1500],
                },
                "ESSENCE_DRAGON":{
                    "flat_damage_vs_ender": [100,200,300,400,500],
                    "mana_after_ender_kill": [100,100,100,100,100,100,100,100,100,100],
                    "fero_vs_dragons": [125,250,500,1000,1500],
                    "inc_zealots_odds": [150,500,1250,2000,3000],
                    "combat_wisdom_in_end": [250,1250,5000],
                    "edrag_cd": [500,1500,2500,3500,4500],
                    "unbridled_rage": [1000,1500,2000,3000,5000],
                    "dragon_reforges_buff": [1500,2250,3250,4500,6500],
                    "increased_sup_chances": [2000],
                },
                "ESSENCE_SPIDER":{
                    "empowered_agility": [50,75,100,150,250,400,750,1000,1750,2500],
                    "vermin_control": [100,500,1000,3000,5000],
                    "bane": [100,500,1000,3000,5000],
                    "spider_training": [250,1250,5000],
                    "toxophilite": [1000,1500,2000,3000,5000]
                },
                "ESSENCE_ICE":{
                    "cold_efficiency": [1000,1500,2000,3000,5000],
                    "cooled_forges": [100,1000,2000,3000,5000],
                    "frozen_skin": [1000,1500,2000,3000,5000],
                },
                "ESSENCE_CRIMSON":{
                    "strongarm_kuudra": [1000,2000],
                    "fresh_tools_kuudra":[200,400,600,800,1000],
                    "headstart_kuudra": [100,200,300,400,500],
                    "master_kuudra": [5000],
                    "fungus_fortuna": [100,200,300,400,500,600,700,800,900,1000],
                    "harena_fortuna":[100,200,300,400,500,600,700,800,900,1000],
                    "crimson_training": [250,1250,5000],
                    "wither_piper": [500,750,1250,2000,3000],
                },
                "ESSENCE_GOLD":{
                    "heart_of_gold": [1000,1500,2000,3000,5000],
                    "treasures_of_the_earth": [150,500,1250,2000,3000],
                    "dwarven_training": [250,1250,5000],
                    "unbreaking": [150,500,1250,2000,3000],
                    "eager_miner": [100,200,300,400,500,600,700,800,900,1000],
                    "midas_lure": [200,400,600,800,1000,1200,1400,1600,1800,2000],
                },
                "ESSENCE_DIAMOND":{
                    "radiant_fisher": [200,400,600,800,1000,1200,1400,1600,1800,2000],
                    "diamond_in_the_rough": [1000,1500,2000,3000,5000],
                    "rhinestone_infusion": [2000],
                    "under_pressure": [125,250,500,1000,1500],
                    "high_roller": [5000],
                    "return_to_sender": [50,75,100,150,250,400,750,1000,1750,2500],
                }
            }

            perks_found = {}
            
            for perkshop in perk_levels:
                for perk in perk_levels[perkshop]:
                    total = sum(perk_levels[perkshop][perk])
                    missing = total - sum(perk_levels[perkshop][perk][:essence_perks[perk]]) if perk in essence_perks else total
                    if perkshop not in perks_found:
                        perks_found[perkshop] = {}
                    perks_found[perkshop][perk] = {
                        "missing":missing,
                        "total":total
                    }
            shops = {}
            for shop in perks_found:
                missing, total = 0, 0
                for perk in perks_found[shop]:
                    missing += perks_found[shop][perk]["missing"]
                    total += perks_found[shop][perk]["total"]
                shops[shop] = {"missing":missing,"total":total}

            bazaar_items = self.bot.hypixel_api.bazaar
            essence_prices = {i:bazaar_items[i]["quick_status"]["sellPrice"] for i in [x for x in shops]}
            total = 0
            for shop in shops:
                total += shops[shop]["missing"]*essence_prices[shop]
            send_string = f"TOTAL COST: **{int(total):,}**\n"
            for shop in shops:
                send_string+=f"{shop}: `{shops[shop]['missing']:,}/{shops[shop]['total']:,}` **({int(shops[shop]['missing']*essence_prices[shop]):,})**\n"
            await interaction.response.send_message(send_string, ephemeral=False) 
            
        except Exception as e:
            traceback.print_exc()
            await interaction.response.send_message(e,ephemeral=True)
        

async def setup(bot: commands.Bot) ->None:
    await bot.add_cog(
        EssenceShop(bot),
        guilds = [discord.Object(id = 804012489955475527)]
    )