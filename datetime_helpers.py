#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:35:32 2026

@author: planetmaker
"""

import datetime

def time_string(time = None):
    if time is None:
        time = datetime.datetime.now()
    return(time.strftime("%d.%m.%Y %H:%Mh"))

def time_string_offset(time = None, offset_hours = 0):
    if time is None:
        time = datetime.datetime.now() + datetime.timedelta(days=offset_hours)
    return(time_string(time))
