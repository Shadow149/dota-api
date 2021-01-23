import json

class Item:
    def __init__(self, itemId):
        self.itemId = itemId

    def get_item_url(self):
        item_json = None
        with open("data/items.json") as item_file:
            item_json = json.load(item_file)

        item_id_json = None
        with open("data/item_ids.json") as item_file:
            item_id_json = json.load(item_file)
        
        if self.itemId == 0:
            return

        item_name = item_id_json[str(self.itemId)]

        return item_json[item_name]["img"]