#!/usr/bin/python
# -*- coding: utf-8 -*-

import gspread


ColumnCount = 5


def zhprint(obj):
    import re
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def refreshData(dataList, initColumn):
    gc = gspread.login('gogobot5566', 'ilovegogobot')
    if initColumn ==0:
        wks = gc.open('gogobotThinkBrian').get_worksheet(1)
    else:
        wks = gc.open('gogobotThinkBrian').get_worksheet(0)
    rowCount = wks.row_count

    
    print ' '
    if initColumn ==1:
        print 'start loading from spreadSheet contributed'
    elif initColumn ==0:
        print 'start loading from spreadSheet protected'

    
    

    data = wks.get_all_values()
    try:
        for r in range(1,rowCount):

            print '*** getting row:',r,' ***'

            newData ={}
            newData['keyword']=[]
            temp = data[r][initColumn]
            tempArray = temp.splitlines()
            for keyword in tempArray:
                if len(keyword)>0:
                    newData['keyword'].append(keyword)

            newData['response']=[]
            temp =data[r][initColumn+1]
            tempArray =temp.splitlines()
            for res in tempArray:
                newData['response'].append(res)

            newData['chance'] = data[r][initColumn+2]

            if('TRUE' in data[r][initColumn+3]):
                newData['commonDia']=True
            else :
                newData['commonDia']=False

            zhprint (newData)

            if len(newData['response'])>0 and len(newData['keyword'])>0 and newData['chance']>0:
                dataList.append(newData)
                print 'data received'
            else:
                print '*** invalid data, dropped ***'

    except:
        print 'end of rows'


def getAction():

    dataList =[]

    # load contributed data first
    refreshData(dataList,1)
    refreshData(dataList,0)

    return dataList




