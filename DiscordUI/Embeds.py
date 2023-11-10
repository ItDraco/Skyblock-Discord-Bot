import discord,json
from datetime import datetime
#from DiscordUI.Buttons import New_View

#{"start":"2022-11-02 00:00","end":"2022-11-03 00:00","data":[random.randint(310000, 400000) for i in range(25)]}
#def GenerateGraph(graph):
#    import pandas as pd
#    import matplotlib.pyplot as plt
#    import matplotlib.dates as mdates
#    idx = pd.date_range(start=graph["start"], end=graph["end"], periods= len(graph["data"]))
#    df = pd.Series([random.randint(310000, 400000) for i in range(len(idx))],  index = idx)
#    fig = plt.figure(num=None, figsize=(7, 4), dpi=80)
#    ax = plt.axes(frameon=False)
#    hours = mdates.HourLocator(interval = 1)
#    h_fmt = mdates.DateFormatter('%H:%M')
#    ax.plot(df.index, df.values, color = 'blue', linewidth = 1, marker = 'o')
#    ax.xaxis.set_major_locator(hours)
#    ax.xaxis.set_major_formatter(h_fmt)
#    fig.autofmt_xdate(rotation=0, ha="center")
#    plt.ylabel('Price')
#    plt.grid(axis='x', color='0.95')
#    plt.grid(axis='y', color='0.95')
#    plt.savefig("graph.png", transparent=True)
#    plt.show()

class Embed:
    def __init__(self, json_embed):
        self.json_embed = json_embed
        self.views = []
        self.created_embeds = self.CreateEmbed(json_embed)
    
    def CreateEmbed(self, json_embed):
        pages = json_embed.get("pages")
        fields = json_embed.get("fields")
        thumbnail = json_embed.get("thumbnail")
        image = json_embed.get("image")
        footer = json_embed.get("footer")
        if pages:
            created_embed = []
            for page in pages:
                created_embed.extend(self.CreateEmbed(page))
            return created_embed
        
        created_embed = discord.Embed(title = json_embed['title'], description = json_embed['description'], color = json_embed['color'])

        if fields:
            for field in fields:
                created_embed.add_field(name = field["name"], value = field["value"], inline = field["inline"])

        if thumbnail:
            created_embed.set_thumbnail(url= thumbnail)

        if image:
            created_embed.set_image(url=image)

        if footer:
            created_embed.set_footer(text = footer , icon_url= "https://cdn.discordapp.com/avatars/856671823873835029/4e29dae869627d4b5ae336ef7ec4b66a.webp?size=128")
            created_embed.timestamp = datetime.utcnow()
        return [created_embed]
