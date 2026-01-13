#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:50:07 2025

@author: planetmaker
"""

import bitjita_api as api
from helpers import read_url_json

cargos_info = api.get_cargos_info()
items_info = api.get_items_info()

def get_info(is_cargo: bool):
    if is_cargo:
        return cargos_info
    return items_info

def get_item_property(what: str, itemID: int, is_cargo = False):
    data = get_info(is_cargo)
    ret = None
    try:
        ret = data.get(itemID).get(what)
    except:
        print("Item {} or property {} not found".format(itemID, what))
    return ret

def get_item_name(itemID: int, is_cargo = False):
    return(get_item_property("name", itemID, is_cargo))

def get_item_tag(itemID: int, is_cargo = False):
    return(get_item_property("tag", itemID, is_cargo))

def get_item_tier(itemID: int, is_cargo = False):
    return(get_item_property("tier", itemID, is_cargo))

def get_item_all(itemID: int, is_cargo = False):
    data = get_info(is_cargo)
    ret = None
    try:
        ret = data.get(itemID)
    except:
        print("Item {} not found".format(itemID))
    return ret

def get_cargo_details(itemID: int):
    if "craftingRecipes" not in cargos_info.get(itemID):
        # sometimes it might be a cargo as available under https://bitjita.com/api/cargo/{}
        detail_data = read_url_json("https://bitjita.com/api/cargo/{}".format(itemID))
        print("Adding details for cargo ID {}".format(itemID))
        for k,v in detail_data.items():
            if k == "cargo":
                continue
            print("Adding: {}: {}".format(k,v))
            cargos_info[itemID][k] = v
    return cargos_info.get(itemID)


def get_item_details(itemID: int, is_cargo=False):
    if is_cargo:
        return get_cargo_details(itemID)

    if "craftingRecipes" not in items_info.get(itemID):
        # sometimes it might be a cargo as available under https://bitjita.com/api/cargo/{}
        detail_data = read_url_json("https://bitjita.com/api/items/{}".format(itemID))
        print("Adding details for item ID {}".format(itemID))
        for k,v in detail_data.items():
            if k == "item":
                continue
            print("Adding: {}: {}".format(k,v))
            items_info[itemID][k] = v
    return items_info.get(itemID)

def get_item_recursive_crafting_requirements(start: dict) -> dict:
    detail_data = get_item_details(start["itemId"])
    try:
        recipes = detail_data.get('craftingRecipes')
        # Make sure we select a recipe which consumes items
        index = 0
        while recipes[index].get['consumedItemStacks'][0].get('item_type') != 'item':
            index += 1
        recipe = recipes[index]
    except:
        recipe = []

    ret = start
    ret["ingredients"] = []
    for ingredient in recipe['consumedItemStacks']:
        ingredient_dict = {'itemId': ingredient['item_id'], 'quantity': ingredient['quantity'], 'ingredients': []}
        get_item_recursive_crafting_requirements(ingredient_dict)
        ret["ingredients"].append(ingredient_dict)
    return(ret)


def get_item_crafting_requirements(itemID: int, amount=1) -> dict:
    ret = {'itemId': itemID, 'amount': amount, 'ingredients': []}
    detail_data = get_item_details(itemID)
    recipe = detail_data.get('craftingRecipes')[0]
    for ingredient in recipe['consumedItemStacks']:
        ret['ingredients'].append({'itemId': ingredient['item_id'], 'quantity': ingredient['quantity'], 'ingredients': []})

    return(ret)

def search_item_by_name(name_str: str):
    ret_list = []
    for entryID, entry in items_info.items():
        if entry["name"].endswith(name_str):
            ret_list.append((entryID, False))
            print("Adding item {} (ID: {})".format(entry["name"], entryID))
    for entryID, entry in cargos_info.items():
        if entry["name"].endswith(name_str):
            ret_list.append((entryID, True))
            print("Adding cargo {} (ID: {})".format(entry["name"], entryID))
    return(ret_list)

def search_item_by_name_and_tag(name_str: str, tag_str: str):
    ret_list = []
    for entryID, entry in items_info.items():
        if entry["name"].endswith(name_str) and tag_str in entry["tag"]:
            ret_list.append((entryID, False))
            print("Adding item {} (ID: {})".format(entry["name"], entryID))
    for entryID, entry in cargos_info.items():
        if entry["name"].endswith(name_str) and tag_str in entry["tag"]:
            ret_list.append((entryID, True))
            print("Adding cargo {} (ID: {})".format(entry["name"], entryID))
    return(ret_list)

def get_item_crafting_info(itemID: int, total_quantity = 1, is_cargo = False):
    ingredients = []
    info = get_item_details(itemID, is_cargo)
    for recipe in info.get('craftingRecipes'):
        name = recipe.get('name')
        if name != "Craft {0}" and name != "Crush {1} into {0}":
            continue
        for item in recipe.get('consumedItemStacks'):
            ingredients.append({
                'itemID': item.get('item_id'),
                'name': get_item_name(item.get('item_id'), api.itemtype_to_isCargo(item.get('item_type'))),
                'quantity': item.get('quantity'),
                'total_quantity': item.get('quantity') * total_quantity,
                'item_type': item.get('item_type'),
                'ingredients': get_item_crafting_info(
                    item.get('item_id'),
                    total_quantity=item.get('quantity') * total_quantity,
                    is_cargo=api.itemtype_to_isCargo(item.get('item_type'))
                    )
                })
    ret = {
        'itemID': itemID,
        'item_type': api.isCargo_to_itemtype(is_cargo),
        'name': get_item_name(itemID, is_cargo),
        'quantity': 1,
        'total_quantity': total_quantity,
        'ingredients': ingredients
        }
    return(ret)
