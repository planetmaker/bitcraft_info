#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 10:03:37 2025

@author: planetmaker
"""

from helpers import read_url_json

def get_url_claim_inventories(claimID: int):
    return("https://bitjita.com/api/claims/{}/inventories".format(claimID))

def get_url_player_inventories(playerID: int):
    return("https://bitjita.com/api/players/{}/inventories".format(playerID))

def get_url_logs(buildingID: int):
    return("https://bitjita.com/api/logs/storage?buildingEntityId={}".format(buildingID))

def get_claim_inventories(claimID: int):
    url = get_url_claim_inventories(claimID)
    return(read_url_json(url))

def get_player_inventories(playerID: int):
    url = get_url_player_inventories(playerID)
    return(read_url_json(url))

def get_claim_aggregate_inventories(claimInventories: dict, buildingIDs = []):
    """
    Format of bitjita API: List of dicts:
    {
        'entityId': '360287970369690701',
        'buildingDescriptionId': 1131063556,
        'buildingName': 'Pristine Stockpile',
        'buildingNickname': 'Holzlager',
        'iconAssetName': 'GeneratedIcons/Other/Buildings/Stockpile/StockpileLargeT6',
        'inventory': [
            {'locked': False, 'volume': 600000,
                   'contents': {'item_id': 3040002, 'quantity': 47, 'item_type': 'item'}
            },
            ...
        ]
    }
    """
    items = {}
    for building in claimInventories["buildings"]:
        entityID = int(building["entityId"])
        if entityID not in buildingIDs:
            continue

        for inventory in building["inventory"]:
            content = inventory["contents"]
            itemID = content["item_id"]
            amount = content["quantity"]
            itemType = content["item_type"]
            if itemID not in items:
                print("Adding new item {} for building {}".format(itemID, entityID))
                items[itemID] = {
                    "quantity": amount,
                    "item_type": itemType
                }
            else:
                items[itemID]["quantity"] += amount

    return(items)

def get_player_itemtype(itemtypeID):
    if itemtypeID == 0:
        return('item')
    if itemtypeID == 1:
        return('cargo')

    return('unknown')

def get_player_aggregate_inventories(playerInventories: dict, inventoryIDs = []):
    """
    Format of Bitjita API: List of dicts:
    {
         'entityId': '360287970233265811',
         'ownerEntityId': '360287970233265811',
         'inventoryName': "Elke's Massive Personal Cache",
         'playerOwnerEntityId': '576460752315736996',
         'pockets': [
             {'locked': False, 'volume': 60000,
                 'contents': {'itemId': 531867890, 'itemType': 0, 'quantity': 29}
             },
             ...
         ]
        'inventoryIndex': 0,
        'cargoIndex': 64,
        'buildingName': 'Town Bank',
        'claimEntityId': '360287970203022237',
        'claimName': 'Twin Falls',
        'claimLocationX': 11270,
        'claimLocationZ': 13872,
        'claimLocationDimension': 1,
        'regionId': 5,
        'inventoryName': 'Town Bank'
    }
    """
    items = {}
    for inventory in playerInventories["inventories"]:
        entityID = int(inventory["entityId"])
        if entityID not in inventoryIDs:
            continue

        # print(inventory)
        for pocket in inventory["pockets"]:
            content = pocket["contents"]
            itemID = content["itemId"]
            amount = content["quantity"]
            itemType = content["itemType"]
            if itemID not in items:
                print("Adding new item {} for inventory {}".format(itemID, entityID))
                items[itemID] = {
                    "quantity": amount,
                    "item_type": get_player_itemtype(itemType)
                }
            else:
                items[itemID]["quantity"] += amount
                # itemType is ignored as it *should* be identical

    return(items)
