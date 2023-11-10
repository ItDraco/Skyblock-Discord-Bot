from Utils import defaults
import re,json,discord,asyncio
class ItemManager:
    def __init__(self, client) -> None:
        self.client = client
        self.stored_items = defaults.GetStoredItems()

    def get_items(self, item_type):
        return self.stored_items[item_type]

    def add_item(self, item_type, new_item):
        self.stored_items[item_type].append(new_item)
        defaults.WriteStoredItems(self.stored_items)
    
    def remove_item(self, item_type, item_to_remove):
        self.stored_items[item_type].remove(item_to_remove)
        defaults.WriteStoredItems(self.stored_items)
    
    def remove_all_items(self, item_type):
        self.stored_items[item_type].clear()
        defaults.WriteStoredItems(self.stored_items)

    def reload_items(self):
        self.stored_items = defaults.GetStoredItems()
