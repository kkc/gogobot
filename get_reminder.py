#!/usr/bin/python
# -*- coding: utf-8 -*-

import gspread


ColumnCount = 5
initColumn = 0

key_WeekOfDay = 'weekofday'
key_Hour = 'hour'
key_min = 'min'
key_msg = 'msg'
key_chance = 'chance'

show_parse_log = False


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def load_data(dataList):
    gc = gspread.login('gogobot5566', 'ilovegogobot')

    wks = gc.open('gogobotReminder').get_worksheet(1)
    rowCount = wks.row_count

    if show_parse_log:
        print 'start loading reminder from spreadSheet ...'

    data = wks.get_all_values()
    try:
        for r in range(1, rowCount):
            if show_parse_log:
                print '***** getting row:', r, ' *****'

            newData = {}
            newData[key_WeekOfDay] = data[r][initColumn]
            newData[key_Hour] = data[r][initColumn + 1]
            newData[key_min] = data[r][initColumn + 2]
            newData[key_chance] = data[r][initColumn + 3]

            newData[key_msg] = []
            tempArray = data[r][initColumn + 4].splitlines()
            for res in tempArray:
                newData[key_msg].append(res)

            zhprint(newData)

            if len(newData[key_WeekOfDay]) > 0 and len(newData[key_Hour]) > 0 and len(newData[key_min]) > 0 and len(
                    newData[key_msg]) > 0 and len(newData[key_WeekOfDay]) > 0:
                dataList.append(newData)
                if show_parse_log:
                    print 'data received'
            else:
                if show_parse_log:
                    print '!!! invalid data, dropped !!!'

    except:
        if show_parse_log:
            print '***** end of rows *****'


def getReminder():
    dataList = []

    load_data(dataList)
    print 'load reminder complete => total reminder count:', len(dataList)

    return dataList


