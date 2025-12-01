#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:38:47 2025

@author: planetmaker
"""

import bitjita_api as api
from helpers import read_url_json
from inventories import inventories_summary
from config import config
from item_type import entities

inventory_summary = inventories_summary()

# So far we only support one claim and one player
bitjita_player_inventories = api.get_player_inventories(config['player_ids'][0][0])
bitjita_claim_inventories  = api.get_claim_inventories(config['claim_ids'][0][0])

claim_inventory_ids = []
for inventory_id in config['claim_inventory_ids']:
    claim_inventory_ids.append(inventory_id[0])
player_inventory_ids = []
for inventory_id in config['player_inventory_ids']:
    player_inventory_ids.append(inventory_id[0])

player_inventories = api.get_player_aggregate_inventories(bitjita_player_inventories, player_inventory_ids)
claim_inventories = api.get_claim_aggregate_inventories(bitjita_claim_inventories, claim_inventory_ids)

for k,v in player_inventories.items():
    inventory_summary.add_item(k,v,source='Player')
for k,v in claim_inventories.items():
    inventory_summary.add_item(k,v,source='Claim')

# cargos_info = api.get_cargos_info()
# items_info = api.get_items_info()
itemscargos = entities()
