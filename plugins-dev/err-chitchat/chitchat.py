# -*- coding: utf8 -*-

# unused args
# pylint: disable-msg=W0613
# no init
# pylint: disable-msg=W0232


"""

errbot plugin - ChitChat

Just messing around~

"""

from errbot import BotPlugin, botcmd
import requests
import json
import random
import sys
import time
import feedparser
import gspread
import copy_strings
import xml.etree.ElementTree as xml
from copy_strings import getAction



reload(sys)
sys.setdefaultencoding("utf-8")

# constants
ShowCompareLog = True
ShowEmoLog = False
ShowTalkHis = True
MaxHistory = 7
LastUpdateTime = 0




emoji = [
    '(allthethings)', '(android)', '(areyoukiddingme)', '(arrington)', '(arya)', '(ashton)', '(atlassian)', '(awthanks)', '(awyeah)', '(badass)', '(badjokeeel)', '(badpokerface)', '(basket)', '(beer)', '(bitbucket)', '(boom)', '(branch)', '(bumble)', '(bunny)', '(cadbury)', '(cake)', '(candycorn)', '(caruso)', '(ceilingcat)', '(cereal)', '(cerealspit)', '(challengeaccepted)', '(chewie)', '(chocobunny)', '(chompy)', '(chris)', '(chucknorris)', '(clarence)', '(coffee)', '(confluence)', '(content)', '(continue)', '(cornelius)', '(daenerys)', '(dance)', '(dealwithit)', '(derp)', '(disapproval)', '(doge)', '(dosequis)', '(drevil)', '(ducreux)', '(dumb)', '(embarrassed)', '(facepalm)', '(failed)', '(firstworldproblem)', '(fonzie)', '(foreveralone)', '(freddie)', '(fry)', '(fuckyeah)', '(fwp)', '(gangnamstyle)', '(garret)', '(gates)', '(ghost)', '(goodnews)', '(greenbeer)', '(grumpycat)', '(gtfo)', '(haveaseat)', '(heart)', '(hipchat)', '(hipster)', '(hodor)', '(huh)', '(ilied)', '(indeed)', '(iseewhatyoudidthere)', '(itsatrap)', '(jackie)', '(jaime)',
    '(jira)', '(jobs)', '(joffrey)', '(jonsnow)', '(kennypowers)', '(krang)', '(kwanzaa)', '(lincoln)', '(lol)', '(lolwut)', '(megusta)', '(menorah)', '(mindblown)', '(ned)', '(nextgendev)', '(ninja)', '(notbad)', '(nothingtodohere)', '(notsureif)', '(notsureifgusta)', '(obama)', '(ohcrap)', '(ohgodwhy)', '(okay)', '(omg)', '(oops)', '(orly)', '(pbr)', '(pete)', '(philosoraptor)', '(pingpong)', '(pirate)', '(pokerface)', '(poo)', '(present)', '(pumpkin)', '(rageguy)', '(rebeccablack)', '(reddit)', '(romney)', '(rudolph)', '(sadpanda)', '(sadtroll)', '(samuel)', '(santa)', '(scumbag)', '(seomoz)', '(shamrock)', '(shrug)', '(skyrim)', '(stare)', '(stash)', '(success)', '(successful)', '(sweetjesus)', '(tableflip)', '(taft)', '(tea)', '(thumbsdown)', '(thumbsup)', '(tree)', '(troll)', '(truestory)', '(trump)', '(turkey)', '(twss)', '(tyrion)', '(tywin)', '(unknown)', '(washington)', '(wat)', '(wtf)', '(yey)', '(yodawg)', '(yougotitdude)', '(yuno)', '(zoidberg)', '(zzz)', '8)', ':#', ':$', ':(', ':)', ':-*', ':D', ':Z', ':o', ':p', ':|', ';)', ';p', '>:-(', 'O:)']


happyString = ['爽', '好笑', '笑死']
sadString = ['受傷', '難過', '生病', '請假', 'Q_Q', 'QQ']
angryString = ['gogobot*爛']

def zhprint(obj):
    import re
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())






class ChitChat(BotPlugin):

    ''' Annoying chit chat plugin
    '''
    min_err_version = '1.6.0'  # Optional, but recommended
    max_err_version = '2.0.0'  # Optional, but recommended
    decayValue = 20
    girl_source = ''

    mMessage = ''

    histMsg = []
    histFrom = []
    histPisiton = 0

    happy = 0
    sad = 0
    angry = 0
    lastCheckTime = 0
    lastLunchTime = 0
    lastDinnerTime = 0
    LastUpdateTime = 0

    action_list = []

    hatedPeopleName = ''
    likePeopleName = ''

    def checkUpdateKeyword(self):
        currentTime = int(time.time())

        print currentTime
        print self.LastUpdateTime


        if  currentTime - self.LastUpdateTime >3600:
            print 'last update > 3600, re-fetch from spreadsheet'
            self.action_list = getAction()
            print 'action updated, total ',len(self.action_list) , 'action now'
            self.LastUpdateTime =currentTime




    def saveHist(self, message, Msgfrom):
        if len(self.histMsg) < MaxHistory:
            self.histMsg.append(message)
            self.histFrom.append(Msgfrom)
        else:
            self.histMsg[self.histPisiton] = message
            self.histFrom[self.histPisiton] = Msgfrom
            print 'memory position: ', self.histPisiton
            if self .histPisiton == MaxHistory - 1:
                self.histPisiton = 0
            else:
                self.histPisiton += 1
        if ShowTalkHis:
            print '**** print hist msg ****'
            for msg in self.histMsg:
                print msg
            print '**** print hist name ****'
            for name in self.histFrom:
                print name
            print '**** end of hist ****'

    def getgirls(self, message):
        a = json.loads(
            requests.get('http://curator.im/api/stream/?token=3b57cbb863364e9eb2f4cd7f833df331&page=' + str(int(random.random() * 140))).content)
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
                otherDes = [u'早上', u'晚上', u'飯', u'上班', u'餐', u'下班', u'出門']

                print 'check weather roll success, keyword matched'
                if self.prevContain(otherDes) or self.checkIfContain(otherDes, message_string):
                    self.showWeahterForcast()
                else:
                    self.showWeahterNow()

                return True
            return False

    def showWeahterNow(self):
        weather = json.loads(
            requests.get('http://api.openweathermap.org/data/2.5/weather?q=taipei&lang=zh_tw').content)

        prefixArray = ['感謝@Duo大大，現在的天氣是', 'hihi~  現在的天氣是', '現在外面天氣是', '外面天氣', '現在外面天氣是', '外面天氣'
                       '因為' + random.choice(self.histFrom) + '的關係，現在的天氣是']
        midfixArray = [' 氣溫是', ',溫度有', '，結果氣溫']
        subfixArray = [
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽',  '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '']
        msg = random.choice(prefixArray) + weather['weather'][0]['description'] + random.choice(
            midfixArray) + str((int(weather['main']['temp']) - 273.15)) + random.choice(subfixArray)
        self.send(self.mMessage.getFrom(), msg,
                  message_type=self.mMessage.getType())

        if u"雨" in weather['weather'][0]['description'] or u"多雲" in weather['weather'][0]['description'] or u"晴" in weather['weather'][0]['description'] and (int(weather['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@duo大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(self.mMessage.getFrom(), random .choice(
                rainNoti), message_type=self.mMessage.getType())

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
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽',  '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '']

        msg = random.choice(prefixArray) + weatherToday['list'][forcastTimeZone]['weather'][0]['description'] + random.choice(
            midfixArray) + str(int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) + random.choice(subfixArray)
        self.send(self.mMessage.getFrom(), msg,
                  message_type=self.mMessage.getType())

        if u"雨" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"多雲" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"晴" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] and (int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@duo大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(self.mMessage.getFrom(), random .choice(
                rainNoti), message_type=self.mMessage.getType())

        # in order to increase chitchat variety, bot will sometimes go off the
        # rail and do something unexpected. sendRandomMessage() insure bot will
        # reply something meaningless occasionally.
    def sendRandomMessage(self):
        if random.randrange(0, 101) > 98:
            print ' **send random message'

            if random .randrange(0, 101) < 65:

                action = random.choice(self.action_list)
                while 'commonDia' in action and action['commonDia'] == False:
                    print ' ***not common dialog, re-roll'
                    action = random.choice(self.action_list)

                totalMessage = random.choice(action['response'])
                response_messages = totalMessage.split('*')

                for msg in response_messages:
                    self.send(self.mMessage.getFrom(),
                              msg,
                              message_type=self.mMessage.getType())
                    print ' **random message "', msg, '" sended'

            else:
                if random.randrange(0, 101) > 50:
                    radReply = ['http://i.imgur.com/DJG1aF4.jpg', 'http://i.imgur.com/ggvWFBo.jpg', 'http://i.imgur.com/xovuE25.jpg'
                                'http://i.imgur.com/uSGbEFG.jpg', 'http://i.imgur.com/mAuzhW9.jpg', 'http://i.imgur.com/8J0DPac.jpg',

                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg)]

                    response_messages = random.choice(radReply).split('*')

                    for msg in response_messages:
                        self.send(self.mMessage.getFrom(),
                                  msg,
                                  message_type=self.mMessage.getType())
                        print ' **random message "', msg, '" sended'

                else:
                    msg = random.choice(emoji)
                    self.send(self.mMessage.getFrom(),
                              msg,
                              message_type=self.mMessage.getType())
                    print ' **random message "', msg, '" sended'

            return True

        return False

    def antiWash(self):
        if len(self.histFrom) < 6:
            return False

        samePerson = True
        firstPesron = self.histFrom[0]
        for name in self.histFrom:
            if firstPesron != name:
                samePerson = False
                break

        if samePerson:
            if random.randrange(0, 101) > 75:
                self.angry += 3
                response = ['可以不要洗版了嗎？', '洗版很好玩嗎？', '不要為了要我回文亂發言好嗎？']
                self.send(self.mMessage.getFrom(), random .choice(
                    response), message_type=self.mMessage.getType())
            else:
                if random.randrange(0, 101) > 80:
                    self.angry += 2
                    self.happy += 3
                    for msg in self.histMsg:
                        self.send(self.mMessage.getFrom(), random .choice(
                                  self. histMsg), message_type=self.mMessage.getType())

        return samePerson

    def printCurrentEmotion(self):
        print '*** print emo ***'
        print 'happy: ', self.happy, 'sad: ', self.sad, 'angry level: ', self.angry
        print '*** lastCheckTime: ', self.lastCheckTime, ' ***'

    def checkIfContain(self, keyArray, message_string):
        for tempString in keyArray:
            keyArray = tempString .split('*')
            tempbool = True

            for key in keyArray:
                # print 'cheking key: ' + key
                if message_string.find(key) == -1:
                    # print 'do not contain ' + key
                    tempbool = False
                    break

            if tempbool:
                return True
        return False

    def checkBadPeople(self, message_string):

        badEnding = [u'拉', u'啦', u'辣']
        response = ['兇屁', '你是在大聲什麼啦！', '你生氣了？？']

        idx = len(message_string) - 1
        for key in badEnding:
            if message_string[idx] == key:

                self.angry += 1
                if random.randrange(0, 101) > 50:
                    self.send(self.mMessage.getFrom(), random.choice(
                        response), message_type=self.mMessage.getType())
                    self.hatedPeopleName = self.mMessage.message.getFrom(
                    ).getResource()
                    return True
                else:
                    return False
        return False

    def updateCurrentEmotion(self, message_string):
        # decay emotion with the time passed

        currentTime = int(time.time())
        timeDiff = currentTime - self.lastCheckTime

        if ShowEmoLog:
            print (timeDiff), 'passed since last update'

        self.happy -= self.decayValue * timeDiff / 3600
        self.sad -= self.decayValue * timeDiff / 3600
        self.angry -= self.decayValue * timeDiff / 3600

        # reset emo if <0
        if self.angry < 0:
            self.angry = 0
        if self.sad < 0:
            self.sad = 0
        if self .happy < 0:
            self.happy = 0
        self.lastCheckTime = int(time.time())

        # update emo with new input
        if self.checkIfContain(happyString, message_string):
            if ShowEmoLog:
                print 'happy str matched: ' + message_string
            self.happy += 1

        if self.checkIfContain(sadString, message_string):
            if ShowEmoLog:
                print 'sad str matched: ' + message_string
            self.sad += 1

        if self.checkIfContain(angryString, message_string):
            if ShowEmoLog:
                print 'angry str matched: ' + message_string
            self.angry += 1





    @botcmd
    def look(self, message, args):
        ''' send gogolook emoji when received command look
        '''
        self.send(message.getFrom(),
                  '(gogolook)',
                  message_type=message.getType())

    def callback_message(self, connection, message):
        ''' Triggered for every received message that isn't coming
            from the bot itself
        '''

        print 'current hour:' + time.strftime("%H")

        message_string = message.getBody().lower()
        message_from = message.getFrom().getResource()
        self.mMessage = message

        self.checkUpdateKeyword()

        if message_from == 'Gogo Bot':
            return

        self.saveHist(message_string, message_from)




        # action can now support multiple keyword and multi-line message
        #
        # actions with complicated keywords should be put on head of action_list
        # or the keyword may never match
        #
        # action_list.append({
        #     'keyword': ['keyword','keyword*keyword2']
        #     'response': ['message1',
        #         'message2_line1*message2_line2'
        #     ], 'chance': chance_int (%)
        # })

        # 亂回機制1
        if self.sendRandomMessage():
            return

        if self.checkBadPeople(message_string):
            return

        if 'Duo Ho' in message_from and random.randrange(0, 101) < 10:
            self.send(message.getFrom(),
                      random.choice(['強', '強！', '丟神！', '霸氣']),
                      message_type=message.getType())

        if self.checkWeather(message_string):
            return

        if self.antiWash():
            return

        if ShowEmoLog:
            print 'emotion before update'
            self.printCurrentEmotion()
        self.updateCurrentEmotion(message_string)
        if ShowEmoLog:
            print 'emotion after update'
            self.printCurrentEmotion()

        if ShowCompareLog:
            print '*** message received, try to responese ***'
            print 'message: ', message_string

        # do not trigger on links
        if 'http:' in message_string or 'https:' in message_string:
            self.sendRandomMessage(self.action_list)
            return

        # start to search if it match any keyword in action_list
        for action in self.action_list:
            if ShowCompareLog:
                print 'see if matched keyword type: ', action['keyword'][0]

            if self.checkIfContain(action['keyword'], message_string):
                if ShowCompareLog:
                    print ' **"', action['keyword'][0], '" matched'

                if 'chance' in action:
                    if ShowCompareLog:
                        zhprint( ' ** '+ action['keyword'] +'has "roll" key, have to roll ')
                    if random .randrange(0, 101) < action['chance']:
                        if ShowCompareLog:
                            print ' **rand < ', action['chance'], ', roll success!!'
                        totalMessage = random.choice(action['response'])
                        response_messages = totalMessage.split('*')

                        for msg in response_messages:
                            self.send(message.getFrom(),
                                      msg,
                                      message_type=message.getType())
                            if ShowCompareLog:
                                print ' **message "', response_messages, '" sended'
                        return
                    elif ShowCompareLog:
                        print ' **rand > ', action['chance'], ', roll failed!'

                else:
                    totalMessage = random.choice(action['response'])
                    response_messages = totalMessage.split('*')

                    for msg in response_messages:
                        self.send(message.getFrom(),
                                  msg,
                                  message_type=message.getType())
                        if ShowCompareLog:
                            zhprint( 'message "'+ response_messages+ '" sended')

                    return

        # 亂回機制2
        if self.sendRandomMessage():
            return

