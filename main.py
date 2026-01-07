#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:38:47 2025

@author: planetmaker
"""

import bitjita_api as api
from inventories import inventories_summary
from config import config
import item_type

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

scholar_items = []
print("Adding Scholar items:\n")
for item in config["scholar_item_search_strings"]:
    sublist = item_type.search_item_by_name_and_tag(item[0], item[1])
    scholar_items.extend(sublist)
print("Adding Scholar cargoes:\n")
for cargo in config["scholar_cargo_search_strings"]:
    sublist = item_type.search_item_by_name(cargo)
    scholar_items.extend(sublist)

(log_detail_elke, log_summary_elke) = api.get_player_logs(config.get('player_ids')[0][0], config.get('claim_ids')[0][0])
print("\nLogs for all inventories of {}:".format(config.get('player_ids')[0][1]))
for k,v in log_summary_elke.items():
    print("{}: {}".format(item_type.get_item_name(k),v))

print("\nAvailable scholar materials:")

with open("scholar_mats.txt", 'w') as f:
    for itemID in scholar_items:
        print("{}, {}, {}, {}".format(item_type.get_item_tier(itemID), item_type.get_item_tag(itemID), item_type.get_item_name(itemID), inventory_summary.get_amount(itemID)))
        f.write("{}, {}, {}, {}\n".format(item_type.get_item_tier(itemID), item_type.get_item_tag(itemID), item_type.get_item_name(itemID), inventory_summary.get_amount(itemID)))
