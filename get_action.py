#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import sys


ColumnCount = 5
show_import_star_log = False
show_log = False


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


# calculate star level, the keyword which has higher star level will be more difficult to be triggered and should be put at head of list
def getStarCount(list):
    total_star_count = 0
    max_star = 0
    keyword_count = 0

    # gogobot is too easy to trigger, assign 0 star to it.
    if len(list) == 1 and list[0] == 'gogobot':
        return 0

    for text in list:
        if text.count('*') > max_star:
            max_star = text.count('*')
        total_star_count += text.count('*')
        keyword_count += 1
    return int(round((max_star + total_star_count) * 30 / keyword_count) + keyword_count) + random.randrange(0, 50)


def refreshData(dataList, tab_index):
    #gc = gspread.login('gogobot5566', 'ilovegogobot')
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Gogobot-b4e12c74d505.json', scope)
    gc = gspread.authorize(credentials)

    inti_col = 0

    if tab_index == 0:
        wks = gc.open('gogobotThinkBrian').get_worksheet(tab_index)
        inti_col = 1
    else:
        wks = gc.open('gogobotThinkBrian').get_worksheet(tab_index)
        inti_col = 0

    rowCount = wks.row_count

    # print ' '

    if tab_index == 1:
        print 'start loading from spreadSheet contributed'
    elif tab_index == 0:
        print 'start loading from spreadSheet protected'

    data = wks.get_all_values()

    try:
        for r in range(1, rowCount):

            if show_log:
                print '*** getting row:', r, ' ***'

            newData = {}
            newData['keyword'] = []
            temp = data[r][inti_col]
            tempArray = temp.splitlines()
            for keyword in tempArray:
                if len(keyword) > 0:
                    newData['keyword'].append(keyword)

            newData['response'] = []
            temp = data[r][inti_col + 1]
            tempArray = temp.splitlines()
            for res in tempArray:
                newData['response'].append(res)

            newData['chance'] = data[r][inti_col + 2]

            if ('TRUE' in data[r][inti_col + 3]):
                newData['commonDia'] = True
            else:
                newData['commonDia'] = False

            if show_log:
                zhprint(newData)

            if len(newData['response']) > 0 and len(newData['keyword']) > 0 and newData['chance'] > 0:
                star_count = getStarCount(newData['response'])
                is_inserted = False

                for i in range(0, len(dataList)):
                    global show_import_star_log
                    if show_import_star_log:
                        print( 'mStar count: ', star_count, 'dataList ', i, ' starCount: ', getStarCount(dataList[i]['keyword']))

                    received_data = dataList[i]
                    if getStarCount(received_data['keyword']) <= star_count:
                        dataList.insert(i, newData)
                        is_inserted = True
                        break

                if not is_inserted:
                    dataList.insert(len(dataList), newData)

                if show_log:
                    print 'data received'
            elif show_log:
                print '*** invalid data, dropped ***'

    except IndexError:
        if show_log:
            print '*** end of lines ***'

        print 'load from tab: ', tab_index, '    total action list size: ', len(dataList)
    except Exception, err:

        print sys.exc_info()[0]


def getAction():
    dataList = []

    refreshData(dataList, 1)
    refreshData(dataList, 2)
    refreshData(dataList, 3)

    # contributed action
    refreshData(dataList, 0)

    return dataList




