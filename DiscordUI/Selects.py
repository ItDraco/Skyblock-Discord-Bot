import discord
from discord import ui
"""
    list of dictionaries
    each dictionary determines what the select option will be.
    label: (text),
    emoji: (emoji),
    value: (value),
    description: (description)
"""
class Dropdown(ui.Select):
    def __init__(self, placeholder:str, options:list, min_values=1, max_values=1):
        discord_select_options = []
        for option in options:
            discord_select_options.append(
                discord.SelectOption(**option))
        super().__init__(placeholder=placeholder, options=discord_select_options, min_values=min_values, max_values=max_values)
    async def callback(self, interaction):
        await interaction.response.send_message(f"you selected {self.values}",ephemeral=True)