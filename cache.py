#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:08:25 2026

@author: planetmaker
"""

import pandas as pd
# from helpers import items_table, claim_members_table, claim_buildings, claim_inventory, player_houses_inventory, player_deployables_inventory
from variables import *
from config import config

cache_path = 'cache/'
filename_items_cache = cache_path + 'items_cache.csv'

def write_cache(what = None):
    if what is None:
        what = config.get('cache')
    if 'items' in what:
        print("Writing items table to {}".format(filename_items_cache))
        global items_table
        items_table.sort_index().to_csv(filename_items_cache, index_label='index')

def read_cache(what = None):
    if what is None:
        what = config.get('cache')
    if 'items' in what:
        global items_table
        try:
            items_table = pd.read_csv(filename_items_cache, index_col='index')
            print("Read items table from {}".format(filename_items_cache))
        except FileNotFoundError:
            print("Cache file does not exist: {}".format(filename_items_cache))
            pass

if __name__ == "__main__":
    read_cache()
