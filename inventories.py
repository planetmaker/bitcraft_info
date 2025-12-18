#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:02:31 2025

@author: planetmaker
"""

class inventories_summary:
    def __init__(self):
        self.origin_ids = set()
        self.items = {}

    def print():
        pass

    def get_amount(self, itemID: int):
        try:
            return(self.items[itemID].get("quantity"))
        except:
            return(0)

    def add_item(self, item_id: int, data: dict, source=None):
        if item_id not in self.items:
            self.items[item_id] = data
        else:
            # assume that the properties are identical when the itemID is identical
            self.items[item_id]["quantity"] += data["quantity"]

        if source is not None:
            self.origin_ids.add(source)
