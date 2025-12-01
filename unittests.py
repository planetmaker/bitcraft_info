#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 13:57:22 2025

@author: planetmaker
"""

import unittest
import bitjita_api as api

class TestBitjitaAPI(unittest.TestCase):

    def test_GetClaimInventories(self):
        claim_inventories = api.get_claim_inventories(360287970203435761)
        self.assertTrue('buildings' in claim_inventories)
        self.assertTrue('entityId' in claim_inventories["buildings"][0])
        self.assertTrue('buildingName' in claim_inventories["buildings"][0])
        self.assertTrue('buildingNickname' in claim_inventories["buildings"][0])
        self.assertTrue('inventory' in claim_inventories["buildings"][0])
        self.assertTrue('contents' in claim_inventories["buildings"][0].get('inventory')[0])
        self.assertTrue('item_id' in claim_inventories["buildings"][0].get('inventory')[0].get('contents'))
        self.assertTrue('quantity' in claim_inventories["buildings"][0].get('inventory')[0].get('contents'))
        self.assertTrue('item_type' in claim_inventories["buildings"][0].get('inventory')[0].get('contents'))

        self.assertTrue('items' in claim_inventories)
        self.assertTrue('id' in claim_inventories["items"][0])
        self.assertTrue('name' in claim_inventories["items"][0])
        self.assertTrue('tag' in claim_inventories["items"][0])
        self.assertTrue('rarity' in claim_inventories["items"][0])
        self.assertTrue('tier' in claim_inventories["items"][0])

        self.assertTrue('cargos' in claim_inventories)
        self.assertTrue('id' in claim_inventories["cargos"][0])
        self.assertTrue('name' in claim_inventories["cargos"][0])
        self.assertTrue('tag' in claim_inventories["cargos"][0])
        self.assertTrue('rarity' in claim_inventories["cargos"][0])
        self.assertTrue('tier' in claim_inventories["cargos"][0])

    def test_GetPlayerInventories(self):
        player_inventories = api.get_player_inventories(576460752315736996)
        self.assertTrue('inventories' in player_inventories)
        self.assertTrue('entityId' in player_inventories.get('inventories')[0])
        self.assertTrue('pockets' in player_inventories.get('inventories')[0])

        for inventory in player_inventories.get('inventories'):
            if inventory.get('entityId') != "360287970233265811": # Massive Personal Chest
                continue
            self.assertTrue('contents' in inventory.get('pockets')[0])
            self.assertTrue('itemId' in inventory.get('pockets')[0].get('contents'))
            self.assertTrue('itemType' in inventory.get('pockets')[0].get('contents'))
            self.assertTrue('quantity' in inventory.get('pockets')[0].get('contents'))

        self.assertTrue('items' in player_inventories)
        self.assertTrue('cargos' in player_inventories)


if __name__ == '__main__':
    unittest.main()