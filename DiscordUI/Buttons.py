import discord
from discord.ui import Button
from DiscordUI.Views import New_View

class PageButton(Button):
    def __init__(self, embeds:list, current_index:int, increment:int, style=discord.ButtonStyle.gray):
        super().__init__(label="<" if increment < 0 else ">", style=style)
        self.embeds=embeds
        self.new_index= (current_index+increment)%len(embeds)
    
    def make_current_new_page(self):
        previous_page = self.embeds.created_embeds[(self.new_index-1)%len(self.embeds)]
        next_page = self.embeds.created_embeds[(self.new_index+1)%len(self.embeds)]
        return previous_page,next_page

    async def callback(self, interaction):
        view = New_View(items=[])
        await interaction.response.edit_message(embed=self.embeds.created_embeds[self.new_index], view=view)

class Default(Button):
    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: str = None, disabled: bool = False, url: str = None, emoji: str = None):
        super().__init__(style = style, label=label, disabled=disabled, url=url, emoji=emoji)

class EmptyButton(Button):
    def __init__(self):
        super().__init__(label="\u200e", style=discord.ButtonStyle.primary)
    async def callback(self, interaction):
        interaction.response.pong

def CreateListOfButtons(dictionary):
    listOfButtons = []
    for button in dictionary["buttons"]:
        if(button["type"]=="pages"):
            listOfButtons.append(PageButton(embed=dictionary, current_index=0, increment=-1))
            listOfButtons.append(PageButton(embed=dictionary, current_index=0, increment=1))
            continue
        if(button["type"]=="empty"):
            listOfButtons.append(EmptyButton())
            continue
    return listOfButtons
        