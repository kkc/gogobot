#!/usr/bin/python
# -*- coding: utf-8 -*-

import gspread


ColumnCount = 5


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def getStarCount(list):
    total_star_count = 0
    max_star = 0
    keyword_count = 0
    for text in list:
        if text.count('*') > max_star:
            max_star = text.count('*')
        total_star_count += text.count('*')
        keyword_count += 1
    return int(round((max_star + total_star_count) * 10 / keyword_count))


def refreshData(dataList, initColumn):
    gc = gspread.login('gogobot5566', 'ilovegogobot')
    if initColumn == 0:
        wks = gc.open('gogobotThinkBrian').get_worksheet(1)
    else:
        wks = gc.open('gogobotThinkBrian').get_worksheet(0)
    rowCount = wks.row_count

    print ' '
    if initColumn == 1:
        print 'start loading from spreadSheet contributed'
    elif initColumn == 0:
        print 'start loading from spreadSheet protected'

    data = wks.get_all_values()

    try:
        for r in range(1, rowCount):

            print '*** getting row:', r, ' ***'

            newData = {}
            newData['keyword'] = []
            temp = data[r][initColumn]
            tempArray = temp.splitlines()
            for keyword in tempArray:
                if len(keyword) > 0:
                    newData['keyword'].append(keyword)

            newData['response'] = []
            temp = data[r][initColumn + 1]
            tempArray = temp.splitlines()
            for res in tempArray:
                newData['response'].append(res)

            newData['chance'] = data[r][initColumn + 2]

            if ('TRUE' in data[r][initColumn + 3]):
                newData['commonDia'] = True
            else:
                newData['commonDia'] = False

            zhprint(newData)

            if len(newData['response']) > 0 and len(newData['keyword']) > 0 and newData['chance'] > 0:
                star_count = getStarCount(newData['response'])
                is_inserted = False

                for i in range(0, len(dataList)):
                    print(
                        'mStar count: ', star_count, 'dataList ', i, ' starCount: ',
                        getStarCount(dataList[i]['keyword']))

                    received_data = dataList[i]
                    if getStarCount(received_data['keyword']) <= star_count:
                        dataList.insert(i, newData)
                        is_inserted = True
                        break

                if not is_inserted:
                    dataList.insert(len(dataList), newData)

                print 'data received'
            else:
                print '*** invalid data, dropped ***'

    except IndexError:
        print '*** end of lines ***'
    except:
        print 'Unexpected error:'


def getAction():
    dataList = []

    # load contributed data first
    # refreshData(dataList, 1)
    refreshData(dataList, 0)

    return dataList




