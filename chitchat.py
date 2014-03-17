# -*- coding: utf8 -*-

# This is a skeleton for Err plugins, use this to get started quickly.

from errbot import BotPlugin, botcmd
from errbot.builtins.webserver import webhook
import requests
import pdb
import json
import random

class ChitChat(BotPlugin):
    ''' Annoying chit chat bot
    '''
    min_err_version = '1.6.0' # Optional, but recommended
    max_err_version = '2.0.0' # Optional, but recommended

    @botcmd                               # this tag this method as a command
    def look(self, message, args):
        self.send(message.getFrom(), \
                          '(gogolook)', \
                          message_type=message.getType())

    def callback_message(self, conn, message):
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
            'keyword': 'kakashi',
            'response': [
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/k.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/ka2.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/kaka3.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/ka2.jpg',
                'https://dl.dropboxusercontent.com/u/3256092/hipchat/k.jpg',
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
            'keyword': '安安',
            'response': [
                '安安 幾歲 住哪 給虧嗎',
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
