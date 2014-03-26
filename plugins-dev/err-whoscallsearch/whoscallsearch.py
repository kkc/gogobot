"""

errbot plugin to do whoscall search

"""

import phonenumbers
import requests
import json

from errbot import BotPlugin, botcmd

class WhosCallSearch(BotPlugin):
    ''' Let's search numbers!
    '''

    @botcmd                               # this tag this method as a command
    def search(self, mess, args):          # it will respond to !hello
        ''' search info for this number
        '''
        print self
        print mess
        e164 = phonenumbers.format_number(phonenumbers.parse(args, 'TW'), \
                                          phonenumbers.PhoneNumberFormat.E164)
        
        yield '(whoscall) searching [' + e164 + ']...'

        # return '/code ' + whoscallsearch.get_default_tag(e164)

        # result = requests.get('https://api.whoscall.com/whoscallsearch/' + \
        #                        e164.replace('+', ''),
        #                  headers={
        #                     "accesstoken": "k7ZI3RH2e9V14D30n4yr2td",
        #                     "userid": "gogobot"
        #                  })
        # result = json.loads(result.content)

        # return '/code ' + json.dumps(result, indent=4)

        # return '/code ' + json.dumps(whoscallsearch.get_tag_suggestions(e164)
        #    , indent=4)

        result = WhosCallSearch.get_tag_suggestions(e164)
        if len(result) <= 0:
            yield 'no info in whoscall database (sadtroll)'
        else:
            yield '/code ' + ' \n'.join(result)

    @staticmethod
    def get_default_tag(e164):
        ''' get default tag from whoscallsearch
        '''
        suggestions =  WhosCallSearch.get_tag_suggestions(e164)
        if len(suggestions) > 0:
            return suggestions[0]
        else:
            return ''

    @staticmethod
    def get_tag_suggestions(e164):
        ''' get tag suggestions from whoscall search
        '''
        result = requests.get('https://api.whoscall.com/whoscallsearch/' + \
                               e164.replace('+', ''),
                         headers={
                            "appid": "def93581",
                            "appkey": "e505f8aa43fd7c5cec81299e4b36c9bf"
                         })
        result = json.loads(result.content)

        suggestions = []

        # partner
        if result['profile']:
            if result['profile']['picurl'] != '':
                suggestions.append(result['profile']['name'])

        if result['topspams'] in ['HFD', 'CALLCENTER']:
            suggestions.append(result['toptag'])

        if result['profile']:
            if result['profile']['name']:
                suggestions.append(result['profile']['name'])
            
        for yellowpage in result['yellowpages']:
            suggestions.append(yellowpage)

        for publictag in result['public_tags']:
            suggestions.append(publictag['tagname'])

        for suggestion in result['suggestiontag'].keys():
            suggestions.append(suggestion)

        return list(set(suggestions))
