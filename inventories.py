#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:02:31 2025

@author: planetmaker
"""

# TODO: Make this class aware that there can be ID collisions between items and cargoes.
# It works now in a make-shift way for the limited amount of items used for scholar town
# expansion purposes, but is not future proof.

import pandas as pd
import tables

import helpers
import bitjita_api as api
import item_type as it
from helpers import items_table, claim_buildings, claim_inventory, player_houses_inventory, player_deployables_inventory

from config import config as config

class inventories_summary:
    def __init__(self):
        self.origin_ids = set()
        self.items = {}

    def print():
        pass

    def get_amount(self, itemID: int, is_cargo = False):
        try:
            return(self.items[itemID].get("quantity"))
        except:
            return(0)


    def get_crafting_amount(self, itemID: int, is_cargo = False):
        return(0)

    def add_item(self, item_id: int, data: dict, source=None):
        if item_id not in self.items:
            self.items[item_id] = data
        else:
            # assume that the properties are identical when the itemID is identical
            self.items[item_id]["quantity"] += data["quantity"]

        if source is not None:
            self.origin_ids.add(source)

def add_inventory_item(inventory: dict, item_id: int, quantity: int, source=None):
    if item_id not in inventory:
        inventory[item_id] = {'quantity': quantity, 'source': set([source])}
    else:
        # assume that the properties are identical when the itemID is identical
        inventory[item_id]["quantity"] += quantity

    if source is not None:
        inventory[item_id]["source"].add(source)

    return(inventory)

# class inventory(dict):
#     def __init__(self, *args, **kw):
#         super(inventory,self).__init__(*args, **kw)
#         self.itemlist = super(inventory,self).keys()
#     def __setitem__(self, key, value):
#         self.itemlist.append(key)
#         super(inventory,self).__setitem__(key, value)


# class inventory_entry():
#     def init(self, item_id: int, quantity = 0, item_type = 'item'):
#         self.item_id = item_id
#         self.quantity = quantity
#         self.item_type = item_type

#     def add(self, quantity):
#         self.quantity += quantity

def add_to_claim_inventory(inventory_id, item_slot):
    global claim_inventory
    item_id = item_slot.get('contents').get('item_id')
    item_type = item_slot.get('contents').get('item_type')
    uid = it.item_uid_from_id(item_id, item_type)
    quantity = item_slot.get('contents').get('quantity')
    tables.df_add_value(claim_inventory, inventory_id, uid, quantity)

def add_building_inventory(building_data):
    building_id = building_data.get('entityId')
    building_type = building_data.get('buildingName')
    building_name = building_data.get('buildingNickname')
    for slot in building_data.get('inventory'):
        add_to_claim_inventory(building_id, slot)


# Read all town storages into a pandas DataFrame
def update_town_inventories(claim_id = config.get('claim_ids')[0][0]):
    url = api.get_url_claim_inventories(claim_id)
    raw_data = helpers.read_url_json(url)
    for building in raw_data.get('buildings'):
        add_building_inventory(building)
    for item in raw_data.get('items'):
        it.add_item_info_from_json(item, False)
    for cargo in raw_data.get('cargos'):
        it.add_item_info_from_json(cargo, True)

if __name__ == "__main__":
    update_town_inventories()
