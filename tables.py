#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:31:17 2026

@author: planetmaker
"""

import pandas as pd

"""
Adding new row with default values to a pandas DataFrame
"""
def df_insert_row(df, uid: str, defaults = None):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("DataFrame required to add rows to.")
        return(df)

    if uid in df.index:
        raise Exception("uid exists already! Nothing added to DataFrame.")
        return(df)


    # Adding row from a pre-defined dict
    if isinstance(defaults, dict):
        try:
            df.loc[uid] = defaults
            return(df)
        except:
            raise Exception("Supplied dict does not match DataFrame. Nothing added to DataFrame.")
            return(df)

    # Adding row with uniform defaults value
    column_names = list(df)
    new_dict = {}
    for item in column_names:
        new_dict[item] = defaults
    df.loc[uid] = new_dict
    return(df)

def df_insert_column(df, name: str, defaults = None):
    if isinstance(defaults, list) and len(defaults) == len(df):
        df[name] = defaults
    else:
        try:
            df[name] = [defaults for _ in range(len(df))]
        except:
            raise
            return(df)
    return(df)

def df_new():
    df = pd.DataFrame({'uid': []})
    df.set_index('uid')
    return(df)

def df_add_value(df, column_name: str, uid: str, quantity: int):
    if uid not in df.index:
        df = df_insert_row(df, uid)
    if column_name not in list(df):
        df = df_insert_column(df, column_name)

    old = df.at[uid, column_name]
    df.at[uid, column_name] = old + quantity
    return(df)

if __name__ == "__main__":
    print("Helper functions for DataFrames. Nothing to do")
