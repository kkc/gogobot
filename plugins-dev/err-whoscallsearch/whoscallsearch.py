# -*- coding: utf8 -*-

# unused args
# pylint: disable-msg=W0613
# no init
# pylint: disable-msg=W0232


"""

errbot plugin - WhosCallSearch

search whoscall database for phone number information

"""

from errbot import BotPlugin, botcmd

import phonenumbers
import requests
import json
from phonenumber_parse import PhonenumberParse


class WhosCallSearch(BotPlugin):
    ''' Let's search numbers!
    '''

    @botcmd
    def search_v6(self, message, args):
        ''' search info for whoscallsearch v6 '''
        args_list = args.split(" ")
        region = args_list[0]
        number = args_list[1]
        numberparse = PhonenumberParse(number, region.upper())

        yield ':whoscall: searching [' + region.upper() + " " + numberparse.e164 + ']...'

        result = self.whoscallsearch_v6(numberparse.e164, region.upper())

        yield result


    @botcmd
    def search_v2(self, message, args):
        ''' search info for this number
        '''
        e164 = phonenumbers.format_number(phonenumbers.parse(args, 'TW'), \
                                          phonenumbers.PhoneNumberFormat.E164)

        yield '(whoscall) searching [' + e164 + ']...'

        result = WhosCallSearch.get_tag_suggestions(e164)
        if len(result) <= 0:
            yield 'no info in whoscall database (sadtroll)'
        else:
            yield '/code ' + ' \n'.join(result)

    @botcmd
    def search(self, message, args):
        e164 = phonenumbers.format_number(phonenumbers.parse(args, 'TW'), \
                                          phonenumbers.PhoneNumberFormat.E164)

        yield '(whoscall) searching [' + e164 + ']...'

        result = WhosCallSearch.whoscallsearch_v3(e164)
        if result['available'] == 1:
            del result['available']
            for (key, value) in result.iteritems():
                yield key + ': ' + value
        else:
            yield 'no info in whoscall database (sadtroll)'

    @botcmd
    def text(self, message, args):
        results = WhosCallSearch.textsearch(args)
        for result in results:
            yield 'title: ' + result['title'] + '\n' + 'address: ' + result['address'] + '\n' + 'number: ' + result['e164']

    @staticmethod
    def textsearch(keyword):
        ''' do textsearch
        '''
        result = requests.get('http://api.dev.whoscall.com:8889/textsearch/' +\
                               keyword,
                         headers={
                            "appid": "def93581",
                            "appkey": "e505f8aa43fd7c5cec81299e4b36c9bf"
                         })
        result = json.loads(result.content)

        return result['results']

    def whoscallsearch_v6(self, e164, region):
        ''' do whoscall search version 6
        '''
        result = requests.get(
            'https://api.whoscall.com/search/v5/%s/%s' % (region, e164),
            headers={
                "userid": "1234",
                "accesstoken": "S84c5m5M73YcR9Z1h93M7i9"
            }
        )

        result = json.loads(result.content)['result']

        data = {}
        data['name'] = result['name']
        data['source'] = result['source']
        data['type'] = result['type']
        data['address'] = result['address']

        response = "Name: %s\n來源: %s\n屬性: %s\n地址: %s\n" % \
            (result['name'], result['source'], result['type'], result['address'])

        return response

    @staticmethod
    def whoscallsearch_v3(e164):
        ''' do whoscall search version 3
        '''
        result = requests.get('https://api.whoscall.com/whoscallsearch/' + \
                               e164.replace('+', '') + '?version=3',
                         headers={
                            "appid": "def93581",
                            "appkey": "e505f8aa43fd7c5cec81299e4b36c9bf"
                         })

        result = json.loads(result.content)

        data = {}
        data['available'] = result['dataavailable']
        data['name'] = result['name']['name']
        data['source'] = result['name']['source']
        data['spam'] = result['spamcategory']['category']
        data['image'] = result['image']
        data['telecom'] = result['telecom']

        return data


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
