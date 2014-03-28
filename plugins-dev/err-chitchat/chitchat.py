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
import xml.etree.ElementTree as xml
reload(sys)
sys.setdefaultencoding("utf-8")

class ChitChat(BotPlugin):
    ''' Annoying chit chat plugin
    '''
    min_err_version = '1.6.0' # Optional, but recommended
    max_err_version = '2.0.0' # Optional, but recommended

    def getgirls(self):
        a=json.loads(requests.get('http://curator.im/api/stream/?token=3b57cbb863364e9eb2f4cd7f833df331&page='+str(int(random.random()*140))).content)
        
        return a['results'][int(random.random()*50)]['thumbnail']
    @botcmd
    def look(self, message, args):
        ''' send gogolook emoji when received command look
        '''
        self.send(message.getFrom(), \
                  '(gogolook)', \
                  message_type=message.getType())

    def callback_message(self, connection, message):
        ''' Triggered for every received message that isn't coming 
            from the bot itself
        '''

        action_list = []

        # action template
        # 
        # action_list.append({
        #     'keyword': '',
        #     'response': [
        #         '',
        #     ]
        # })

        action_list.append({
            'keyword': '(thumbsup)',
            'response': [
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/like.png',
                '',
            ]
        })

        action_list.append({
            'keyword': 'gogolook',
            'response': [
                '(gogolook)',
                ''
            ]
        })

        action_list.append({
            'keyword': 'kakashi',
            'response': [
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/k.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/k.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/ka2.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/ka2.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/ka2.jpg',
                '',
                ''
            ]
        })

        action_list.append({
            'keyword': u'吃飯飯',
            'response': [
                json.loads(
                    requests.get('http://more.handlino.com/sentences.json?'\
                                     'limit=27').content
                )['sentences'][0],
            ]
        })

        action_list.append({
            'keyword': u'看正妹',
            'response': [
                self.getgirls()
            ]
        })

        action_list.append({
            'keyword': '安安',
            'response': [
                '安安 幾歲 住哪',
                ' ',
                ' ',
                '(troll)',
            ]
        })

        action_list.append({
            'keyword': '@gogobot',
            'response': [
                '(pokerface)',
                '(areyoukiddingme)',
                '(lol)',
                '(troll)',
                '(wat)', 
                '(wtf)',
                '(content)',
                '(ohcrap)',
                '(derp)',
                '(dumb)',
                '(poo)',
                ''
            ]
        })

        action_list.append({
            'keyword': 'gogobot',
            'response': [
                u'有人找我嗎 (fuckyeah)',
                '(pokerface)',
                '',
                '(dumb)',
            ]
        })

        message_string = message.getBody().lower()
        message_from = message.getFrom().getResource()
        print 'got message [' + message_string + '] from [' + message_from + ']'

        for action in action_list:
            if message_string.find(action['keyword']) != -1:
                response_message = random.choice(action['response'])
                self.send(message.getFrom(), \
                          response_message, \
                          message_type=message.getType())
                return
