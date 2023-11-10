import asyncio, copy, os
from Api.auction import GetAuctions
from Api.bazaar import GetBazaar
from Utils.auction_handling import FetchAuctionItems, SortAuctionItems, NotifyAuctionItems, ConvertDictToFormatedFile, DeleteNotifiedAuctions
from Utils.bazaar import FetchBazaarItems, NotifyBazaarItems

class HypixelApi():
    def __init__(self, client) ->None:
        self.api_key = os.environ.get('hypixel_api_key')
        self.client = client
        self.running = True
        self.auctions = []
        self.bazaar = []
        self.notified_auction_ids = []
        self.notified_bazaar = []
    
    async def update_data(self):
        asyncio.gather(
            self.update_auctions(),
            self.update_bazaar()
        )

    async def update_auctions(self):
        while self.running:
            wanted_items = copy.deepcopy(self.client.item_manager.get_items("auctions"))
            self.auctions = GetAuctions()
            found_items= FetchAuctionItems(self.auctions, wanted_items)
            found_items = SortAuctionItems(found_items)
            #ConvertDictToFormatedFile(found_items)
            item_ids = await NotifyAuctionItems(found_items, self.client, self.notified_auction_ids)
            await DeleteNotifiedAuctions(self.client, self.notified_auction_ids, item_ids)
            await asyncio.sleep(80)

    async def update_bazaar(self):
        while self.running:
            #wanted_items = copy.deepcopy(self.client.item_manager.get_items("bazaar"))
            self.bazaar = GetBazaar()
            # found_items, notify_items = FetchBazaarItems(self.bazaar, wanted_items)
            await asyncio.sleep(25)