#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:58:00 2026

@author: planetmaker
"""

import tables

if 'tables_defined' not in locals():
    tables_defined = True
    items_table = tables.df_new()
    claim_members_table = tables.df_new()
    claim_buildings = tables.df_new()
    claim_inventory = tables.df_new()
    player_houses_inventory = tables.df_new()
    player_deployables_inventory = tables.df_new()
    player_log_table = tables.df_new()

def init():
    global items_table
    global claim_members_table
    global claim_buildings
    global claim_inventory
    global player_houses_table
    global player_deployables_inventory
    global player_log_table

    items_table = tables.df_new()
    claim_members_table = tables.df_new()
    claim_buildings = tables.df_new()
    claim_inventory = tables.df_new()
    player_houses_inventory = tables.df_new()
    player_deployables_inventory = tables.df_new()
    player_log_table = tables.df_new()
