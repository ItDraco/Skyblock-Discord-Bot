import discord
from discord import ui

class Modal(ui.Modal):
    def __init__(self, *, title: str):
        super().__init__(title=title)
    #hex_code = ui.TextInput(label="Hex Code", style=discord.TextStyle.short, required=True, min_length=6, max_length=6)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"This modal does nothing.")
