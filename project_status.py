#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:38:47 2025

@author: planetmaker
"""

from config import config
import tables
import item_type as it
from variables import *
import inventories
import cache

if __name__ == "__main__":
    global claim_inventory
    cache.read_cache()
    project_inventory = tables.df_new()
    output_columns = ['name', 'tag', 'tier']
    for column in output_columns:
        tables.df_insert_column(project_inventory, column)
    inventories.update_town_inventories()
    project_inventory.loc[:,'claim'] = claim_inventory.sum(axis=1)
    project_inventory = it.add_item_info_to_table(project_inventory, column_names = output_columns)
    project_inventory.to_csv(config.get('filename_townupgrade'),index_label='index')
    cache.write_cache()
