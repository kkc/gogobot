# -*- coding: utf8 -*-

# unused args
# pylint: disable-msg=W0613
# no init
# pylint: disable-msg=W0232


"""

errbot plugin - ChitChat

Just messing around~

"""

import json
import random
import threading
import time
import datetime
from time import strftime

import sys
from errbot import BotPlugin, botcmd
import requests
from get_action import getAction
from get_reminder import getReminder, key_WeekOfDay, key_Hour, key_min, key_msg, key_chance


reload(sys)
sys.setdefaultencoding("utf-8")

MaxHistory = 40
LastUpdateTime = 0

emoji = [
    '(allthethings)', '(android)', '(areyoukiddingme)', '(arrington)', '(arya)', '(ashton)', '(atlassian)',
    '(awthanks)', '(awyeah)', '(badass)', '(badjokeeel)', '(badpokerface)', '(basket)', '(beer)', '(bitbucket)',
    '(boom)', '(branch)', '(bumble)', '(bunny)', '(cadbury)', '(cake)', '(candycorn)', '(caruso)', '(ceilingcat)',
    '(cereal)', '(cerealspit)', '(challengeaccepted)', '(chewie)', '(chocobunny)', '(chompy)', '(chris)',
    '(chucknorris)', '(clarence)', '(coffee)', '(confluence)', '(content)', '(continue)', '(cornelius)', '(daenerys)',
    '(dance)', '(dealwithit)', '(derp)', '(disapproval)', '(doge)', '(dosequis)', '(drevil)', '(ducreux)', '(dumb)',
    '(embarrassed)', '(facepalm)', '(failed)', '(firstworldproblem)', '(fonzie)', '(foreveralone)', '(freddie)',
    '(fry)', '(fuckyeah)', '(fwp)', '(gangnamstyle)', '(garret)', '(gates)', '(ghost)', '(goodnews)', '(greenbeer)',
    '(grumpycat)', '(gtfo)', '(haveaseat)', '(heart)', '(hipchat)', '(hipster)', '(hodor)', '(huh)', '(ilied)',
    '(indeed)', '(iseewhatyoudidthere)', '(itsatrap)', '(jackie)', '(jaime)',
    '(jira)', '(jobs)', '(joffrey)', '(jonsnow)', '(kennypowers)', '(krang)', '(kwanzaa)', '(lincoln)', '(lol)',
    '(lolwut)', '(megusta)', '(menorah)', '(mindblown)', '(ned)', '(nextgendev)', '(ninja)', '(notbad)',
    '(nothingtodohere)', '(notsureif)', '(notsureifgusta)', '(obama)', '(ohcrap)', '(ohgodwhy)', '(okay)', '(omg)',
    '(oops)', '(orly)', '(pbr)', '(pete)', '(philosoraptor)', '(pingpong)', '(pirate)', '(pokerface)', '(poo)',
    '(present)', '(pumpkin)', '(rageguy)', '(rebeccablack)', '(reddit)', '(romney)', '(rudolph)', '(sadpanda)',
    '(sadtroll)', '(samuel)', '(santa)', '(scumbag)', '(seamoz)', '(shamrock)', '(shrug)', '(skyrim)', '(stare)',
    '(stash)', '(success)', '(successful)', '(sweetjesus)', '(tableflip)', '(taft)', '(tea)', '(thumbsdown)',
    '(thumbsup)', '(tree)', '(troll)', '(truestory)', '(trump)', '(turkey)', '(twss)', '(tyrion)', '(tywin)',
    '(unknown)', '(washington)', '(wat)', '(wtf)', '(yey)', '(yodawg)', '(yougotitdude)', '(yuno)', '(zoidberg)',
    '(zzz)', '8)', ':#', ':$', ':(', ':)', ':-*', ':D', ':Z', ':o', ':p', ':|', ';)', ';p', '>:-(', 'O:)']

happyString = ['爽', '好笑', '笑死']
sadString = ['受傷', '難過', '生病', '請假', 'Q_Q', 'QQ']
angryString = ['gogobot*爛']

mMessage = -1
mMessageTime = 0

mReminder = ''


# time gap in sec, if you changed this value, plz change TimerThread gap 'if' constrain accordingly
# default value: 300
timeGap = 300


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def checkTime(hour, min):
    mHour = datetime.datetime.now().hour
    mMinute = datetime.datetime.now().minute

    if mHour >= int(hour) and mHour < int(hour) + 1 and mMinute >= int(min) and mMinute < int(min) + (timeGap / 60):
        return True
    else:
        return False


def checkDay(days_of_week):
    day_list = list(days_of_week)
    for d in day_list:
        if datetime.datetime.today().weekday() == int(d):
            return True
    return False


class ChitChat(BotPlugin):
    ''' Annoying chit chat plugin
    '''
    min_err_version = '1.6.0'  # Optional, but recommended
    max_err_version = '2.1.0'  # Optional, but recommended
    decayValue = 20
    girl_source = ''

    histMsg = []
    histFrom = []
    histPisiton = 0

    happy = 0
    sad = 0
    angry = 0
    lastCheckTime = 0
    lastLunchTime = 0
    lastDinnerTime = 0

    isCheckThreadStarted = False


    # log control
    ShowCompareLog = True
    ShowEmoLog = False
    ShowTalkHis = True
    ShowAntiWash = True
    show_reminder_log = True

    UpdateActionInterval = 3600
    LastUpdateTime = 0

    action_list = []

    hatedPeopleName = ''
    likePeopleName = ''

    noteList = []

    # mSelf =''

    def send_from_messages(self, message_list):
        msg = random.choice(message_list)

        msg = msg.replace('randname', '@' + random.choice(self.histFrom).replace(' ', ''))
        msg = msg.replace('randmsg', random.choice(self.histMsg))

        self.send(mMessage.getFrom(), msg, message_type=mMessage.getType())

        if self.ShowCompareLog:
            zhprint(' **message "' + msg + '" sended')


    # this thread check schedule and response
    class TimerThread(threading.Thread):

        mChitChat = ''

        def __init__(self, chitchat_self):
            print '** checking thread started **'
            threading.Thread.__init__(self)
            self.mChitChat = chitchat_self


        def run(self):
            while (True):
                print '** check reminder: ', strftime("%Y-%m-%d %H:%M:%S", ), ' **'

                # weather forecast
                if ( checkTime(9, 10) or checkTime(12, 30) or checkTime(19, 10)) and \
                        checkDay('01234') and random.randrange(0, 101) > 98:
                    print 'show weather forecast reminder'
                    self.mChitChat.showWeahterForcast()

                # meetup reminder
                # TODO

                # auto talkonButtonClickListener
                if (int(time.time()) - mMessageTime) > 3600 * 20 and datetime.datetime.now().hour > 10 \
                        and datetime.datetime.now().hour < 20 and random.randrange(0, 101) < 3 and checkDay('01234'):
                    askMsg = ['吃飯啊', '走了 吃飯啊', '有人要吃東西嗎', '吃飯吃飯吃飯吃飯吃飯', '都沒有人要跟我完', '有人在嗎？？', '幫我開門', '肚子餓了', '大家還在嗎？',
                              '怎麼這麼久都沒有人留言？', '大家好，我是googbot', '都沒人留言 大家都放假去了嗎？', '今天天氣不錯']
                    self.mChitChat.send_from_messages(askMsg)

                    global mMessageTime
                    mMessageTime = int(time.time())


                # load reminder from spreadsheet
                reminder = getReminder()
                for r in reminder:
                    match_day = checkDay(r[key_WeekOfDay])
                    match_time = checkTime(r[key_Hour], r[key_min])

                    if self.mChitChat.show_reminder_log:
                        check_status = ''
                        if match_day:
                            check_status += '  day matched(' + r[key_WeekOfDay] + ')   '
                        else:
                            check_status += '  day not matched(' + r[key_WeekOfDay] + ')   '

                        if match_time:
                            check_status += 'time matched(' + r[key_Hour] + ':' + r[key_min] + ')'
                        else:
                            check_status += 'time not matched(' + r[key_Hour] + ':' + r[key_min] + ')'

                        zhprint('reminder check: ' + r[key_msg][0] + check_status)

                    if match_day and match_time:
                        print '**time matched**'

                        if random.randrange(0, 101) < int(r[key_chance]):
                            print 'roll < ' + r[key_chance] + ', success!'

                            self.mChitChat.send_from_messages(r[key_msg])

                        else:
                            print 'roll > ' + r[key_chance] + ', failed!'


                # setting status is not working on gogobot??

                # if random.randrange(0, 101) < 100:
                # print '** change status **'
                # selfStatus = ['/available 希望的種子', '/available 我不是網軍', '/available 心情不好 QQ', '/available 期待你來給我安慰',
                # '/available 驚奇4曹仁', '/available 驚奇4曹仁', '/available 驚奇4曹仁', '/available 魏延既出，司馬難追 ',
                # '/available 司馬當活馬醫', '/available 乳搖知馬力-日久變人妻', '/available 你真的很閒 沒事看我的狀態']
                #
                # if mMessage != -1:
                #
                # print self.mChitChat
                # print mMessage
                #
                # self.mChitChat.send(mMessage.getFrom(), random.choice(selfStatus), message_type=mMessage.getType())
                # print 'changed status'

                time.sleep(timeGap)


    def loadCurrentNote(self):
        file = open('user/Document/gogobot/gogobot.sav', 'w+')


    def saveCurrentNote(self):
        file = open('user/Document/gogobot/gogobot.sav', 'w+')
        jsonFile = json.load(file)


    def checkUpdateKeyword(self):
        currentTime = int(time.time())

        difference = (currentTime - self.LastUpdateTime )

        if difference > self.UpdateActionInterval:
            print 'last update more than a hour, re-fetch from spreadsheet: ', difference
            self.action_list = getAction()
            print 'action updated, total ', len(self.action_list), 'action now'
            self.LastUpdateTime = currentTime


    def saveHist(self, message, Msgfrom):
        if len(self.histMsg) < MaxHistory:
            self.histMsg.append(message)
            self.histFrom.append(Msgfrom)
        else:
            self.histMsg[self.histPisiton] = message
            self.histFrom[self.histPisiton] = Msgfrom
            print 'memory position: ', self.histPisiton
            if self.histPisiton == MaxHistory - 1:
                self.histPisiton = 0
            else:
                self.histPisiton += 1
        if self.ShowTalkHis:

            print '**** printing hist msg ****'
            histMsg = []

            for msg in self.histMsg:
                histMsg.append(msg)
            i = 0
            for name in self.histFrom:
                histMsg[i] = name + ' said:  ' + histMsg[i]
                i = i + 1

            for msg in histMsg:
                zhprint(msg)

            print '**** end of hist ****'


    def getgirls(self, message):
        a = json.loads(
            requests.get('http://curator.im/api/stream/?token=3b57cbb863364e9eb2f4cd7f833df331&page=' + str(
                int(random.random() * 140))).content)
        index = int(random.random() * 50)
        self.girl_source = "小海嚴選正妹 - " + \
                           a['results'][index]['name'] + " - " + a['results'][index]['url']

        return a['results'][index]['image']


    # check if previous talk contain keyword
    def prevContain(self, keywordArray):
        for key in keywordArray:
            for prevMsg in self.histMsg:
                if key in prevMsg:
                    return True
        return False


    def checkWeather(self, message_string):
        if random.randrange(0, 11) < 2:
            return False
        else:

            if self.checkIfContain([u'天氣', u'氣溫'], message_string):
                # otherDes = [u'早上', u'晚上', u'飯', u'上班', u'餐', u'下班', u'出門']
                #
                # print 'check weather roll success, keyword matched'
                # if self.prevContain(otherDes) or self.checkIfContain(otherDes, message_string):
                # self.showWeahterForcast()
                # else:

                self.showWeahterForcast()

                return True
            return False


    def showWeahterNow(self):
        weather = json.loads(
            requests.get('http://api.openweathermap.org/data/2.5/weather?q=taipei&lang=zh_tw').content)

        prefixArray = ['感謝@Duo大大，現在的天氣是', 'hihi~  現在的天氣是', '現在外面天氣是', '外面天氣', '現在外面天氣是', '外面天氣'
                                                                                         '因為' + random.choice(
            self.histFrom) + '的關係，現在的天氣是']
        midfixArray = [' 氣溫是', ',溫度有', '，結果氣溫', '，然後氣溫是']
        subfixArray = [
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽', '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '有夠冷', '令人打了個韓戰', '記得多加件外套',
            '度，外出多加注意歐', '度，不要忘了防曬歐', '度，真是冷死人了', '度，不是很適合出門', '，真想待在家裡不出門....', '', '', '']
        msg = random.choice(prefixArray) + weather['weather'][0]['description'] + random.choice(
            midfixArray) + str((int(weather['main']['temp']) - 273.15)) + random.choice(subfixArray)
        self.send(mMessage.getFrom(), msg,
                  message_type=mMessage.getType())

        if u"雨" in weather['weather'][0]['description'] or u"多雲" in weather['weather'][0]['description'] \
                or u"晴" in weather['weather'][0]['description'] and (int(weather['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@duo大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(mMessage.getFrom(), random.choice(
                rainNoti), message_type=mMessage.getType())


    def showWeahterForcast(self):
        weatherToday = json.loads(
            requests.get('http://api.openweathermap.org/data/2.5/forecast?q=taipei&lang=zh_tw').content)

        currentTime = int(time.strftime("%H"))
        forcastTimeZone = 0

        if currentTime < 4:
            prefixArray = ['明天上班天氣是', '明天早上上班天氣是', 'hihi 明天早上上班天氣是']
            forcastTimeZone = 0
        elif currentTime < 10:
            prefixArray = ['今天上班天氣是', '上班外面天氣是']
            forcastTimeZone = 0
        elif currentTime < 13:
            prefixArray = [
                '中午吃飯天氣是', '中午外面天氣', '中午吃飯天氣是', '中午外面天氣', '感謝@Duo大大，今天中午吃飯的天氣是']
            forcastTimeZone = 1
        elif currentTime < 17:
            prefixArray = ['今天下班天氣是', 'hihi 下班外面天氣是']
            forcastTimeZone = 3
        else:
            prefixArray = ['今天晚上天氣是', '晚上外面天氣是']
            forcastTimeZone = 4

        midfixArray = [' 氣溫是', ',溫度有', '，結果氣溫']
        subfixArray = [
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽', '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '']

        msg = random.choice(prefixArray) + weatherToday['list'][forcastTimeZone]['weather'][0][
            'description'] + random.choice(
            midfixArray) + str(int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) + random.choice(
            subfixArray)
        self.send(mMessage.getFrom(), msg,
                  message_type=mMessage.getType())

        if u"雨" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"多雲" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"晴" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] and (
                    int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@duo大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(mMessage.getFrom(), random.choice(
                rainNoti), message_type=mMessage.getType())


    # in order to increase chitchat variety, bot will sometimes go off the rail and do something unexpected.
    # sendRandomMessage() insure bot will reply something meaningless occasionally.
    def checkSendRandomMessage(self):
        if random.randrange(0, 101) > 98:
            print ' **send random message'

            if random.randrange(0, 101) < 75:

                action = random.choice(self.action_list)
                while 'commonDia' in action and action['commonDia'] == False:
                    print' ***not common dialog, re-roll'
                    action = random.choice(self.action_list)

                totalMessage = random.choice(action['response'])
                response_messages = totalMessage.split('*')

                for msg in response_messages:
                    self.send(mMessage.getFrom(),
                              msg,
                              message_type=mMessage.getType())
                    print' **random message "', msg, '" sended'

            else:
                if random.randrange(0, 101) > 50:
                    radReply = ['http://i.imgur.com/DJG1aF4.jpg', 'http://i.imgur.com/ggvWFBo.jpg', 'http://i.imgur.com/xovuE25.jpg',
                                'http://i.imgur.com/uSGbEFG.jpg', 'http://i.imgur.com/mAuzhW9.jpg', 'http://i.imgur.com/8J0DPac.jpg',
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg)]

                    response_messages = random.choice(radReply).split('*')

                    for msg in response_messages:
                        self.send(mMessage.getFrom(), msg, message_type=mMessage.getType())
                        print' **random message "', msg, '" sended'

                else:
                    msg = random.choice(emoji)
                    self.send(mMessage.getFrom(), msg, message_type=mMessage.getType())
                    print' **random message "', msg, '" sended'

            return True

        return False


    def antiWash(self):
        return False

        # remove antiwash function

        if len(self.histFrom) - self.histPisiton < 7:
            return False

        samePerson = True
        firstPesron = self.histFrom[self.histPisiton]

        i = self.histPisiton
        while i > 0 and i > self.histPisiton - 7:
            if firstPesron != self.histFrom[i]:
                print 'name', self.histFrom[i]
                samePerson = False
                i -= 1
                break

        if samePerson:
            if random.randrange(0, 101) > 75:
                self.angry += 3
                response = ['可以不要洗版了嗎？', '洗版很好玩嗎？', '不要為了要我回文亂發言好嗎？', '人的忍耐是有限度的！']
                self.send(mMessage.getFrom(), random.choice(response), message_type=mMessage.getType())
            else:
                if random.randrange(0, 101) > 80:
                    self.angry += 2
                    self.happy += 3
                    i = 0
                    for msg in self.histMsg:
                        self.send(mMessage.getFrom(), random.choice(self.histMsg), message_type=mMessage.getType())
                        i += 1
                        if i > 7:
                            return True

        return samePerson


    def printCurrentEmotion(self):
        print '*** print emo ***'
        print 'happy: ', self.happy, 'sad: ', self.sad, 'angry level: ', self.angry
        print'*** lastCheckTime: ', self.lastCheckTime, ' ***'


    def checkIfContain(self, keyArray, message_string):
        # total key array
        for key in keyArray:
            keyArray_ = key.split('*')
            tempbool = True

            # must match every key in keyArray_
            for key_ in keyArray_:
                # print 'cheking key: ' + key
                if 'randname' in key_:
                    tempbool2 = False
                    tempString = ''

                    # match one of name in hisFrom
                    for hisName in self.histFrom:
                        tempString = key_.replace('randname', hisName)
                        if tempString in message_string:
                            tempbool2 = True
                            break

                    if tempbool2 != True:
                        tempbool = False


                elif not (key_ in message_string):
                    # print 'do not contain ' + key
                    tempbool = False
                    break

            if tempbool:
                return True
        return False


    # check if people speak in bad temper,
    def checkBadPeople(self, message_string):
        badEnding = [u'拉', u'啦', u'辣']
        response = ['兇屁', '你是在大聲什麼啦！', '你生氣了？？']

        idx = len(message_string) - 1
        for key in badEnding:
            if message_string[idx] == key:

                self.angry += 1
                if random.randrange(0, 101) > 50:
                    self.send(mMessage.getFrom(), random.choice(response), message_type=mMessage.getType())
                    self.hatedPeopleName = mMessage.message.getFrom().getResource()
                    return True
                else:
                    return False
        return False


    def updateCurrentEmotion(self, message_string):
        # decay emotion with the time passed

        currentTime = int(time.time())
        timeDiff = currentTime - self.lastCheckTime

        if self.ShowEmoLog:
            print (timeDiff), 'passed since last update'

        self.happy -= self.decayValue * timeDiff / 3600
        self.sad -= self.decayValue * timeDiff / 3600
        self.angry -= self.decayValue * timeDiff / 3600

        # reset emo if <0
        if self.angry < 0:
            self.angry = 0
        if self.sad < 0:
            self.sad = 0
        if self.happy < 0:
            self.happy = 0
        self.lastCheckTime = int(time.time())

        # update emo with new input
        if self.checkIfContain(happyString, message_string):
            if self.ShowEmoLog:
                print 'happy str matched: ' + message_string
            self.happy += 1

        if self.checkIfContain(sadString, message_string):
            if self.ShowEmoLog:
                print 'sad str matched: ' + message_string
            self.sad += 1

        if self.checkIfContain(angryString, message_string):
            if self.ShowEmoLog:
                print 'angry str matched: ' + message_string
            self.angry += 1


    def checkGogobotCmd(self, message):
        # reload all action list
        if 'gogoreload' in message:
            print 'COMMDAND RECEIVED: reload action list'
            self.LastUpdateTime = 0
            self.send = self.send(mMessage.getFrom(), 'command received, reloading', message_type=mMessage.getType())

            return

        if 'gogoreset' in message:
            print 'COMMDAND RECEIVED: reset memory'
            self.histFrom = []
            self.histMsg = []
            self.send(mMessage.getFrom(), 'command received, history is now clean', message_type=mMessage.getType())

        if 'gogoshowcompare' in message:
            if self.ShowCompareLog == True:
                self.ShowCompareLog = False
            else:
                self.ShowCompareLog = True
            print 'COMMDAND RECEIVED: ShowCompareLog set to ', self.ShowCompareLog

        if 'gogoshowhist' in message:
            if self.ShowTalkHis == True:
                self.ShowTalkHis = False
            else:
                self.ShowTalkHis = True
            print 'COMMDAND RECEIVED: ShowTalkHis set to ', self.ShowCompareLog

        if 'gogotest' in message:
            self.send(mMessage.getFrom(), '@NickJian', message_type=mMessage.getType())
            print 'COMMDAND RECEIVED: gogotest'

        if 'gogowash' in message:
            if self.ShowAntiWash:
                self.ShowAntiWash = False
            else:
                self.ShowAntiWash = True

            self.send(mMessage.getFrom(), 'antiwash status is now :' + self.ShowAntiWash, message_type=mMessage.getType())
            print 'COMMDAND RECEIVED: antiwash status is now :', self.ShowAntiWash

        if 'gogoremindlog' in message:

            if self.show_reminder_log:
                self.show_reminder_log = False
            else:
                self.show_reminder_log = True
            self.send(mMessage.getFrom(), 'gogoremindlog status is now :' + self.ShowAntiWash,
                      message_type=mMessage.getType())


    @botcmd
    def look(self, message, args):
        ''' send gogolook emoji when received command look
        '''
        self.send(message.getFrom(),
                  '(gogolook)',
                  message_type=message.getType())


    # def checkWantRemind(self, message):
    # if u'提醒我' in message:
    # message.replace(u'提醒我', '')
    # if u'點' in message or u'分' in message:
    # message.
    #
    #
    # else:
    # self.send(mMessage.getFrom(), random.choice(
    # '你沒說時間啊？'), message_type=mMessage.getType())
    # else:
    # return False




    def callback_message(self, connection, message):

        # ###### pre-process #######


        message_string = message.getBody().lower()
        message_from = message.getFrom().getResource()

        print message_from
        print message_string

        if message_from == 'Gogo Bot':
            return

        global mMessage
        mMessage = message
        global mMessageTime
        mMessageTime = int(time.time())



        # non-gogobot response part, maybe custom gogobot command or some bug proof code.
        self.checkGogobotCmd(message_string)
        self.checkUpdateKeyword()

        self.saveHist(message_string, message_from)


        # start checking thread if snot started yet
        if not self.isCheckThreadStarted:
            mThread = self.TimerThread(self)
            mThread.start()
            self.isCheckThreadStarted = True

        # ###### gogobot response part #######


        # if self.checkWantRemind(message_string):
        # return

        # random response #1
        if self.checkSendRandomMessage():
            return

        # do not trigger on links
        if 'http:' in message_string or 'https:' in message_string:
            self.checkSendRandomMessage()
            return

        if self.checkBadPeople(message_string):
            return

        if 'Duo Ho' in message_from and random.randrange(0, 101) < 10:
            self.send(message.getFrom(),
                      random.choice(['強', '強！', '丟神！', '霸氣']),
                      message_type=message.getType())

        if self.checkWeather(message_string):
            return

        if self.ShowAntiWash and self.antiWash():
            return

        if self.ShowEmoLog:
            print 'emotion before update'
            self.printCurrentEmotion()
        self.updateCurrentEmotion(message_string)
        if self.ShowEmoLog:
            print 'emotion after update'
            self.printCurrentEmotion()

        if self.ShowCompareLog:
            print '*** message received, try to responese ***'
            print 'message: ', message_string

        counter = 0
        Appendedkeyword = ''

        # start to search if it match any keyword in action_list
        print '****** start to check action *****'
        for action in self.action_list:
            if self.ShowCompareLog:
                if counter < 10:
                    counter += 1
                    Appendedkeyword = Appendedkeyword + action['keyword'][0] + ", "
                else:
                    print 'check keywords: ', Appendedkeyword
                    counter = 0
                    Appendedkeyword = ' '

            if self.checkIfContain(action['keyword'], message_string):
                if self.ShowCompareLog:
                    print '"', action['keyword'][0], '" matched'

                if 'chance' in action:
                    if self.ShowCompareLog:
                        zhprint(' ** ' + ''.join(action['keyword']) + 'has roll-key, have to roll ')
                    if random.randrange(0, 101) < int(action['chance']):
                        if self.ShowCompareLog:
                            print ' **rand < ', action['chance'], ', roll success!!'
                        totalMessage = random.choice(action['response'])
                        response_messages = totalMessage.split('*')

                        self.send_from_messages(response_messages)

                        return
                    elif self.ShowCompareLog:
                        print ' **rand > ', action['chance'], ', roll failed!'

                else:
                    totalMessage = random.choice(action['response'])
                    response_messages = totalMessage.split('*')

                    self.send_from_messages(response_messages)
                    return


        # random response #2
        if self.checkSendRandomMessage():
            return

        if self.ShowCompareLog and counter != 0:
            print 'chceck keyword: ', Appendedkeyword

        print '****** end checking action *****'

