#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 10:52:06 2025

@author: planetmaker
"""

import requests

def read_url_json(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        return(response.json())

    print("Error loading inventories from URL: ", url)
    return({})

def add_inventory_dicts(a: dict, b: dict):
    ret_dict = a
    for entry in b:
        if entry not in a:
            ret_dict[entry] = b[entry]
            continue

        for item in b[entry]:
            ret_dict[entry][item] += 3

            # buildings:
            # 'contents': {'item_id': 3040002, 'quantity': 47, 'item_type': 'item'}
            # pockets:
            # 'contents': {'itemId': 5110026, 'itemType': 0, 'quantity': 10}