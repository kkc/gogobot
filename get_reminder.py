#!/usr/bin/python
# -*- coding: utf-8 -*-

import gspread


ColumnCount = 5
initColumn = 0

key_WeekOfDay = 'weekofday'
key_Hour = 'hour'
key_min = 'min'
key_msg = 'msg'
key_workonly = 'workonly'


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def refreshData(dataList):
    gc = gspread.login('gogobot5566', 'whoscall123')

    wks = gc.open('gogobotReminder').get_worksheet(1)
    rowCount = wks.row_count

    print 'start loading reminder from spreadSheet ...'
    data = wks.get_all_values()
    try:
        for r in range(1, rowCount):

            print '*** getting row:', r, ' ***'

            newData = {}
            newData[key_WeekOfDay] = data[r][initColumn]
            newData[key_Hour] = data[r][initColumn + 1]
            newData[key_min] = data[r][initColumn + 2]

            newData[key_msg] = []
            newData[key_msg].append(data[r][initColumn + 3])

            if 'TRUE' in data[r][initColumn + 4]:
                newData[key_workonly] = True
            else:
                newData[key_workonly] = False

            zhprint(newData)

            if len(newData[key_WeekOfDay]) > 0 and len(newData[key_Hour]) > 0 and len(newData[key_min]) > 0 and len(
                    newData[key_msg]) > 0 and len(newData[key_WeekOfDay]) > 0:
                dataList.append(newData)
                print 'data received'
            else:
                print '!!! invalid data, dropped !!!'

    except:
        print 'end of rows'


def getReminder():
    dataList = []

    refreshData(dataList)

    return dataList




