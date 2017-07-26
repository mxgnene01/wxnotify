#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Meng xiangguo <mxgnene01@gmail.com>
#
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        2017/7/24  下午5:55

def fetchall_as_dict(cursor):
    """fetch all cursor results and returns them as a list of dicts"""
    names = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    if rows:
        return [dict(zip(names, row)) for row in rows]
    else:
        return []


def fetchone_as_dict(cursor):
    """fetch one cursor results and returns them as a list of dicts"""
    names = [x[0] for x in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(names, row))
    else:
        return None
