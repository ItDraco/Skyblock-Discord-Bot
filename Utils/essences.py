import requests,json

x = requests.get("https://sky.shiiyu.moe/api/v2/profile/deathstreeks")
x = x.json()
for profile in x["profiles"]:
    if x["profiles"][profile]["current"]:
        print(json.dumps(x["profiles"][profile]["raw"]["perks"],indent=4))

perks = {
    "Undead Shop":{
        "catacombs_boss_luck": [100,1000,10000,100000],   
        "catacombs_looting": [1000,2000,3000,4000,5000],
        "revive_stone": [200000],
        "catacombs_health": [1000,2500,5000,10000,25000],      
        "catacombs_defense": [1000,4000,6000,8000,10000],     
        "catacombs_intelligence": [1000,4000,6000,8000,10000],
        "catacombs_strength": [1000,4000,6000,8000,10000],
        "catacombs_crit_damage": [1000,3000,10000,20000,50000],
    },
    "Wither Shop":{
        "permanent_health": [100,250,500,1000,1500],
        "permanent_defense": [100,250,500,1000,1500],
        "permanent_speed": [100,250,500,1000,1500],
        "permanent_intelligence": [100,250,500,1000,1500],
        "forbidden_blessing": [200,400,600,800,1000,1200,1400,1600,1800,2000],
        "permanent_strength": [100,250,500,1000,1500],
    },
    "Dragon Shop":{
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
    "Spider Shop":{
        "empowered_agility": [50,75,100,150,250,400,750,1000,1750,2500],
        "vermin_control": [100,500,1000,3000,5000],
        "bane": [100,500,1000,3000,5000],
        "spider_training": [250,1250,5000],
        "toxophilite": [1000,1500,2000,3000,5000]
    },
    "Ice Shop":{
        "cold_efficiency": [1000,1500,2000,3000,5000],
        "cooled_forges": [100,1000,2000,3000,5000],
        "frozen_skin": [1000,1500,2000,3000,5000],
    },
    "Crimson Shop":{
        "strongarm_kuudra": [1000,2000],
        "fresh_tools_kuudra":[200,400,600,800,1000],
        "headstart_kuudra": [100,200,300,400,500],
        "master_kuudra": [5000],
        "fungus_fortuna": [100,200,300,400,500,600,700,800,900,1000],
        "harena_fortuna":[100,200,300,400,500,600,700,800,900,1000],
        "crimson_training": [250,1250,5000],
        "wither_piper": [500,750,1250,2000,3000],
    },
    "Gold Shop":{
        "heart_of_gold": [1000,1500,2000,3000,5000],
        "treasures_of_the_earth": [150,500,1250,2000,3000],
        "dwarven_training": [250,1250,5000],
        "unbreaking": [150,500,1250,2000,3000],
        "eager_miner": [100,200,300,400,500,600,700,800,900,1,000],
        "midas_lure": [200,400,600,800,1000,1200,1400,1600,1800,2000],
    },
    "Diamond Shop":{
        "radiant_fisher": [200,400,600,800,1000,1200,1400,1600,1800,2000],
        "diamond_in_the_rough": [1000,1500,2000,3000,5000],
        "rhinestone_infusion": [2000],
        "under_pressure": [125,250,500,1000,1500],
        "high_roller": [5000],
        "return_to_sender": [50,75,100,150,250,400,750,1000,1750,2500],
    }
}

perks = {
    "catacombs_boss_luck": [100,1000,10000,100000],   
    "catacombs_looting": [1000,2000,3000,4000,5000],     
    "permanent_intelligence": [100,250,500,1000,1500],
    "forbidden_blessing": [200,400,600,800,1000,1200,1400,1600,1800,2000],   
    "permanent_strength": [100,250,500,1000,1500],    
    "permanent_defense": [100,250,500,1000,1500],     
    "permanent_health": [100,250,500,1000,1500],      
    "permanent_speed": [100,250,500,1000,1500],       
    "catacombs_health": [1000,2500,5000,10000,25000],      
    "catacombs_defense": [1000,4000,6000,8000,10000],     
    "catacombs_intelligence": [1000,4000,6000,8000,10000],
    "catacombs_strength": [1000,4000,6000,8000,10000],
    "catacombs_crit_damage": [1000,3000,10000,20000,50000],
    "revive_stone": [200000],
    "combat_wisdom_in_end": [250,1250,5000],
    "inc_zealots_odds": [150,500,1250,2000,3000],
    "flat_damage_vs_ender": [100,200,300,400,500],
    "edrag_cd": [500,1500,2500,3500,4500],
    "fero_vs_dragons": [125,250,500,1000,1500],
    "cold_efficiency": [1000,1500,2000,3000,5000],
    "spider_training": [250,1250,5000],
    "bane": [100,500,1000,3000,5000],
    "cooled_forges": [100,1000,2000,3000,5000],
    "empowered_agility": [50,75,100,150,250,400,750,1000,1750,2500],
    "vermin_control": [100,500,1000,3000,5000],
    "headstart_kuudra": [100,200,300,400,500],
    "strongarm_kuudra": [1000,2000],
    "dragon_reforges_buff": [1500,2250,3250,4500,6500],
    "fresh_tools_kuudra":[200,400,600,800,1000],
    "harena_fortuna": [100,200,300,400,500,600,700,800,900,1000],
    "fungus_fortuna": [100,200,300,400,500,600,700,800,900,1000],
    "mana_after_ender_kill": [100,100,100,100,100,100,100,100,100,100],
    "crimson_training": [250,1250,5000],
    "master_kuudra": [5000],
    "season_of_joy": [200,400,800,1500,2100,3000,3000,4000,4000,4000],
    "wither_piper": [500,750,1250,2000,3000],
    "increased_sup_chances": [2000],
    "frozen_skin": [1000,1500,2000,3000,5000],
    "return_to_sender": [50,75,100,150,250,400,750,1000,1750,2500],
    "radiant_fisher": [200,400,600,800,1000,1200,1400,1600,1800,2000],
    "diamond_in_the_rough": [1000,1500,2000,3000,5000],
    "rhinestone_infusion": [2000],
    "heart_of_gold": [1000,1500,2000,3000,5000],
    "unbreaking": [150,500,1250,2000,3000],
    "midas_lure": [200,400,600,800,1000,1200,1400,1600,1800,2000],
    "unbridled_rage": [1000,1500,2000,3000,5000],
    "under_pressure": [125,250,500,1000,1500],
    "high_roller": [5000],
    "treasures_of_the_earth": [150,500,1250,2000,3000],
    "eager_miner": [100,200,300,400,500,600,700,800,900,1,000],
    "dwarven_training": [250,1250,5000],
    "toxophilite": [1000,1500,2000,3000,5000]
}