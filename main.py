#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:38:47 2025

@author: planetmaker
"""

import datetime

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
    if len(sublist) != 10:
        print("Not found all 10 tiers for cargo: {}".format(cargo))
        print(sublist)
    scholar_items.extend(sublist)

for (playerID, playerName, playerConfig) in config.get('player_ids'):
    if not playerConfig.get('printLog'):
        continue
    (log_details_player, log_summary_player) = api.get_player_logs(playerID, playerName)
    print("\nLogs for all inventories of {}:".format(playerName))
    for k,v in log_summary_player.items():
        print("{}: {}".format(item_type.get_item_name(k),v))

print("\nAvailable scholar materials:")

with open("scholar_mats.txt", 'w') as f:
    f.write("{}, {}, {}, {}\n".format(0, "Stand:", datetime.datetime.now().strftime('"Update: %d.%m.%Y %H:%Mh"'), 0))
    for (itemID, is_cargo) in scholar_items:
        print("{}, {}, {}, {}".format(item_type.get_item_tier(itemID, is_cargo), item_type.get_item_tag(itemID, is_cargo), item_type.get_item_name(itemID, is_cargo), inventory_summary.get_amount(itemID, is_cargo)))
        f.write("{}, {}, {}, {}\n".format(item_type.get_item_tier(itemID, is_cargo), item_type.get_item_tag(itemID, is_cargo), item_type.get_item_name(itemID, is_cargo), inventory_summary.get_amount(itemID, is_cargo)))
