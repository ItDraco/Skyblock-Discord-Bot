from discord.ui import View

class New_View(View):
    def __init__(self, items: list):
        super().__init__(timeout=60)
        for item in items:
            self.add_item(item)
