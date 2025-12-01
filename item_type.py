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
        return(elf.get("tag", itemID))

    def get_tier(self, itemID: int):
        return(self.get("tier", itemID))


