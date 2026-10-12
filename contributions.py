#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:15:25 2026

@author: planetmaker
"""
import pandas as pd
import datetime as dt
import tables
import item_type as it

import bitjita_api as api
from config import config
from helpers import read_url_json, player_log_table
import datetime_helpers as dth


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

def new_series(player_name, building_type, shape):
    entries = [player_name, building_type] + [0 for _ in range(shape[0]-2)]
    return(pd.Series(entries))

def add_item_to_dataframe(df, item_id, item_type, quantity, building_type, player_name):
    column_name = player_name + building_type
    row_name = item_id
    try:
        old_quantity = df.at[row_name, column_name]
    except:
        old_quantity = 0
    if not column_name in df.columns:
        series = new_series(player_name, building_type, df.shape)
        df.assign(player_name,series)
    return(df)

def add_player_storage_logs_to_DataFrame(df, player_log):
    results_chests = dict()
    results_barters = dict()
    for log in player_log['logs']:
        player_name = log['subjectName']
        sign = storagetype_to_sign(log['data'].get('type'))
        quantity = log['data'].get('quantity')
        item_id = log['data'].get('item_id')
        item_type = log['data'].get('item_type')
        uid = it.item_uid_from_id(item_id, item_type)
        df = tables.df_add_value(df, player_name, uid, quantity * sign)
        # building_type = building_to_buildingtype(log['building'])
        # add_item_to_dataframe(df, item_id, item_type, sign * quantity, building_type, player_name)
    return(df)

if __name__ == "__main__":
    player_log_table = tables.df_new()
    player_log_table = tables.df_insert_column(player_log_table, 'Item Name')
    player_log_table = tables.df_insert_column(player_log_table, 'Tag')

    for player_config in config.get('player_ids'):
        if not player_config[2].get('printLog'):
            continue

        player_id = player_config[0]
        time_since_string = dth.time_string_offset(offset_hours = -config.get('days_backlog'))

        player_url_logs = api.get_url_player_logs(player_id)
        player_log = read_url_json(player_url_logs)
        player_log_table = add_player_storage_logs_to_DataFrame(player_log_table, player_log)

        # print(player_url_logs)
        # print(player_log)
