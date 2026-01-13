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

def get_url_storage_logs(buildingID: int):
    return("https://bitjita.com/api/logs/storage?buildingEntityId={}".format(buildingID))

def get_url_player_logs(playerID: int, limit=1000, since="2025-11-01T00:00:00Z"):
    return("https://bitjita.com/api/logs/storage?playerEntityId={}&limit={}&since={}".format(playerID, limit, since))

def get_url_items_info(search_str = None):
    url = "https://bitjita.com/api/items"
    if search_str is not None:
        url.join("?=")
        url.join(e for e in search_str if e.isalnum())
    return url

def get_url_cargos_info(search_str = None):
    url = "https://bitjita.com/api/cargo"
    if search_str is not None:
        url.join("?=")
        url.join(e for e in search_str if e.isalnum())
    return url

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

def get_items_info(search_str = None):
    url = get_url_items_info(search_str)

    data = read_url_json(url)
    ret_dict = {}
    for entry in data["items"]:
        key = int(entry["id"])
        # rate limit is 250 request / minute on bitjita. This needs to be slowed down
        # data_detail = read_url_json(url + '/{}'.format(key))
        ret_dict[key] = entry
        ret_dict[key].pop("id")
    return(ret_dict)

def get_item_name(itemID: int):
    string = ""
    return string

def get_cargos_info(search_str = None):
    url = get_url_cargos_info(search_str)

    data = read_url_json(url)
    ret_dict = {}
    for entry in data["cargos"]:
        key = int(entry["id"])
        # rate limit is 250 request / minute on bitjita. This needs to be slowed down
        # data_detail = read_url_json(url + '/{}'.format(key))
        ret_dict[key] = entry
        ret_dict[key].pop("id")
    return(ret_dict)

def get_player_logs(playerID:int, claimID: int, limit=1000, since="2025-12-01T00:00:00Z"):
    per_storage = {}
    summary = {}
    url = get_url_player_logs(playerID, limit=limit, since=since)
    raw_logs = read_url_json(url)
    for entry in raw_logs.get("logs"):
        quantity = entry.get("data").get("quantity")
        quantity = quantity * (1 if entry.get("data").get("type") == "deposit_item" else -1)
        itemID   = entry.get("data").get("item_id")
        storageID = entry.get("objectEntityId")

        if storageID not in per_storage:
            per_storage[storageID] = {}
        if itemID not in per_storage.get(storageID):
            per_storage[storageID][itemID] = quantity
        else:
            per_storage[storageID][itemID] += quantity

        if itemID not in summary:
            summary[itemID] = quantity
        else:
            summary[itemID] += quantity

    return (per_storage, summary)

def get_player_itemtype(itemtypeID):
    if itemtypeID == 0:
        return('item')
    if itemtypeID == 1:
        return('cargo')

    return('unknown')

def isCargo_to_itemtype(is_cargo):
    if is_cargo:
        return('cargo')
    return('item')

def itemtype_to_isCargo(itemtype):
    if itemtype == 'item':
        return(False)
    return(True)

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
