#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:50:07 2025

@author: planetmaker
"""

import bitjita_api as api
from helpers import read_url_json

class entities:
    def __init__(self):
        cargos_info = api.get_cargos_info()
        items_info = api.get_items_info()
        self.stuff = cargos_info | items_info

    def get(self, what: str, itemID: int):
        ret = None
        try:
            ret = self.stuff.get(itemID).get(what)
        except:
            print("Item {} or property {} not found".format(itemID, what))
        return ret

    def get_name(self, itemID: int):
        return(self.get("name", itemID))

    def get_tag(self, itemID: int):
        return(self.get("tag", itemID))

    def get_tier(self, itemID: int):
        return(self.get("tier", itemID))

    def get_all(self, itemID: int):
        ret = None
        try:
            ret = self.stuff.get(itemID)
        except:
            print("Item {} not found".format(itemID))
        return ret

    def get_details(self, itemID: int):
        if "craftingRecipes" not in self.stuff.get(itemID):
            # sometimes it might be a cargo as available under https://bitjita.com/api/cargo/{}
            detail_data = read_url_json("https://bitjita.com/api/items/{}".format(itemID))
            print("Adding details for ID {}".format(itemID))
            for k,v in detail_data.items():
                if k == "item":
                    continue
                print("Adding: {}: {}".format(k,v))
                self.stuff[itemID][k] = v
        return self.stuff.get(itemID)

    def get_recursive_crafting_requirements(self, start: dict) -> dict:
        detail_data = self.get_details(start["itemId"])
        try:
            recipes = detail_data.get('craftingRecipes')
            # Make sure we select a recipe which consumes items
            index = 0
            while recipes[index].get['consumedItemStacks'][0].get('item_type') != 'item':
                index += 1
            recipe = recipes[index]
        except:
            recipe = []

        ret = start
        ret["ingredients"] = []
        for ingredient in recipe['consumedItemStacks']:
            ingredient_dict = {'itemId': ingredient['item_id'], 'quantity': ingredient['quantity'], 'ingredients': []}
            self.get_recursive_crafting_requirements(ingredient_dict)
            ret["ingredients"].append(ingredient_dict)
        return(ret)


    def get_crafting_requirements(self, itemID: int, amount=1) -> dict:
        ret = {'itemId': itemID, 'amount': amount, 'ingredients': []}
        detail_data = self.get_details(itemID)
        recipe = detail_data.get('craftingRecipes')[0]
        for ingredient in recipe['consumedItemStacks']:
            ret['ingredients'].append({'itemId': ingredient['item_id'], 'quantity': ingredient['quantity'], 'ingredients': []})

        return(ret)

    def search_by_name_and_tag(self, name_str: str, tag_str: str):
        ret_list = []
        for entryID, entry in self.stuff.items():
            if entry["name"].endswith(name_str) and tag_str in entry["tag"]:
                ret_list.append(entryID)
                print("Adding {} (ID: {})".format(entry["name"], entryID))
        return(ret_list)


