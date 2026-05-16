#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:15:25 2026

@author: planetmaker
"""
import pandas as pd
from datetime import datetime
import datetime_helpers as dth
import tables
import item_type as it

import bitjita_api as api
from config import config
from helpers import read_url_json, player_log_table, items_table



def storagetype_to_sign(storage_type: str):
    if storage_type == 'withdraw_item':
        return(-1)
    if storage_type == 'deposit_item':
        return(1)
    print("Unknown storage type: {}".format(storage_type))
    return(0)

def building_to_buildingtype(building):
    name = building.get('buildingName')
    if 'Chest' in name:
        return('Chest')
    if 'Barter Stall' in name:
        return('Barter')
    if 'Item Storage' in name:
        return('Storage')
    if 'Cargo Bin' in name:
        return('Bin')
    if 'Stockpile' in name:
        return('Stockpile')
    if 'Hexite Reserve' in name:
        return('Reserve')
    print("Unhandled building type: {}".format(name))
    return("")

def add_player_storage_logs_to_DataFrame(df, player_log):
    results_chests = dict()
    results_barters = dict()
    try:
        for log in player_log['logs']:
            player_name = log['subjectName']
            sign = storagetype_to_sign(log['data'].get('type'))
            quantity = log['data'].get('quantity')
            item_id = log['data'].get('item_id')
            item_type = log['data'].get('item_type')
            uid = it.item_uid_from_id(item_id, item_type)
            df = tables.df_add_value(df, player_name, uid, quantity * sign)
    except:
        print("Empty log given")
        pass
    return(df)

def add_player_to_DataFrame(player):
    global claim_members_table
    player_entity_id = player.get('playerEntityId')
    name = player.get('userName')
    perm_inventory = bool(player.get('inventoryPermission'))
    perm_build = bool(player.get('buildPermission'))
    perm_officer = bool(player.get('officerPermission'))
    perm_coowner = bool(player.get('coOwnerPermission'))
    try:
        last_login = datetime.strptime(player.get('lastLoginTimestamp'), "%Y-%m-%d %H:%M:%S+00")
    except:
        last_login = None
    claim_members_table.at[player_entity_id, 'name'] = name
    claim_members_table.at[player_entity_id, 'perm_inventory'] = perm_inventory
    claim_members_table.at[player_entity_id, 'perm_build'] = perm_build
    claim_members_table.at[player_entity_id, 'perm_officer'] = perm_officer
    claim_members_table.at[player_entity_id, 'perm_coowner'] = perm_coowner
    claim_members_table.at[player_entity_id, 'last_login'] = last_login

if __name__ == "__main__":
    global player_log_table
    global claim_members_table
    player_log_table = tables.df_new()
    player_log_table = tables.df_insert_column(player_log_table, 'Item Name')
    player_log_table = tables.df_insert_column(player_log_table, 'Tag')

    claim_members_table = tables.df_new()
    url = api.get_url_claim_members(config.get('claim_ids')[0][0])
    raw_data = read_url_json(url)
    for player in raw_data.get('members'):
        print("Adding {}".format(player.get('userName')))
        add_player_to_DataFrame(player)

    time_since_string = dth.time_string_offset(offset_hours = -config.get('days_backlog')*24)
    for player_id in claim_members_table.index:
        # if not player_config[2].get('printLog'):
        #     continue

        player_url_logs = api.get_url_player_logs(player_id, since=time_since_string)
        player_log = read_url_json(player_url_logs)
        player_log_table = add_player_storage_logs_to_DataFrame(player_log_table, player_log)
        print("Added Logs for {} ({} entries)".format(claim_members_table[player_id, 'name'], len(player_log.get('logs'))))

    # Add items from the item table provided along with the logs
    for item in player_log.get('items'):
        it.add_item_info_from_json(item, False)
    for cargo in player_log.get('cargos'):
        it.add_item_info_from_json(cargo, True)

    # Populate the item info
    for i,row in player_log_table.iterrows():
        uid = i
        try:
            name = it.items_table['name', uid]
            tag = it.items_table['tag', uid]
        except:
            print("Item ID not found in table: {}".format(uid))
            is_cargo, item_id = it.item_id_from_uid(uid)
            if is_cargo:
                url = api.get_url_cargo_by_id(item_id)
                raw_data = read_url_json(url).get('cargo')

            else:
                url = api.get_url_item_by_id(item_id)
                raw_data = read_url_json(url).get('item')

            it.add_item_info_from_json(raw_data, is_cargo)
            name = raw_data.get('name')
            tag = raw_data.get('tag')
            # name = it.items_table['name', uid]

        player_log_table = tables.df_set_value(player_log_table, 'Item Name', uid, name)
        player_log_table = tables.df_set_value(player_log_table, 'Tag', uid, tag)

    player_log_table.to_csv(config.get('filename_contributions'))
        # print(player_url_logs)
        # print(player_log)
