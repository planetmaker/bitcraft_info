#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:02:31 2025

@author: planetmaker
"""

# TODO: Make this class aware that there can be ID collisions between items and cargoes.
# It works now in a make-shift way for the limited amount of items used for scholar town
# expansion purposes, but is not future proof.

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
