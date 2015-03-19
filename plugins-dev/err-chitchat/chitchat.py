# -*- coding: utf8 -*-

# unused args
# pylint: disable-msg=W0613
# no init
# pylint: disable-msg=W0232


"""

errbot plugin - ChitChat

Just messing around~

"""
import urllib
import json
import random
import threading
import time
import datetime
from time import strftime
from subprocess import call

import re
import sys
from errbot import BotPlugin, botcmd
import requests
from get_action import getAction
from get_reminder import getReminder, key_WeekOfDay, key_Hour, key_min, key_msg, key_chance


reload(sys)
sys.setdefaultencoding("utf-8")

# how many lines of dialog will gogobot remember
MaxHistory = 50

# how many lines of dialog will gogobot consider it as message to gogobot itself
MaxComprehensiveLine = 4

LastUpdateTime = 0

emoji = [':bowtie:', ':smile:', ':laughing:', ':blush:', ':smiley:', ':relaxed:', ':smirk:', ':heart_eyes:', ':kissing_heart:',
         ':kissing_closed_eyes:', ':flushed:', ':relieved:', ':satisfied:', ':grin:', ':wink:', ':stuck_out_tongue_winking_eye:',
         ':stuck_out_tongue_closed_eyes:', ':grinning:', ':kissing:', ':kissing_smiling_eyes:', ':stuck_out_tongue:', ':sleeping:',
         ':worried:', ':frowning:', ':anguished:', ':open_mouth:', ':grimacing:', ':confused:', ':hushed:', ':expressionless:',
         ':unamused:', ':sweat_smile:', ':sweat:', ':disappointed_relieved:', ':weary:', ':pensive:', ':disappointed:', ':confounded:',
         ':fearful:', ':cold_sweat:', ':persevere:', ':cry:', ':sob:', ':joy:', ':astonished:', ':scream:', ':neckbeard:',
         ':tired_face:', ':angry:', ':rage:', ':triumph:', ':sleepy:', ':yum:', ':mask:', ':sunglasses:', ':dizzy_face:', ':imp:',
         ':smiling_imp:', ':neutral_face:', ':no_mouth:', ':innocent:', ':alien:', ':yellow_heart:', ':blue_heart:', ':purple_heart:',
         ':heart:', ':green_heart:', ':broken_heart:', ':heartbeat:', ':heartpulse:', ':two_hearts:', ':revolving_hearts:', ':cupid:',
         ':sparkling_heart:', ':sparkles:', ':star:', ':star2:', ':dizzy:', ':boom:', ':collision:', ':anger:', ':exclamation:',
         ':question:', ':grey_exclamation:', ':grey_question:', ':zzz:', ':dash:', ':sweat_drops:', ':notes:', ':musical_note:',
         ':fire:', ':hankey:', ':poop:', ':shit:', ':+1:', ':thumbsup:', ':-1:', ':thumbsdown:', ':ok_hand:', ':punch:', ':facepunch:',
         ':fist:', ':v:', ':wave:', ':hand:', ':raised_hand:', ':open_hands:', ':point_up:', ':point_down:', ':point_left:',
         ':point_right:', ':raised_hands:', ':pray:', ':point_up_2:', ':clap:', ':muscle:', ':metal:', ':fu:', ':walking:', ':runner:',
         ':running:', ':couple:', ':family:', ':two_men_holding_hands:', ':two_women_holding_hands:', ':dancer:', ':dancers:',
         ':ok_woman:', ':no_good:', ':information_desk_person:', ':raising_hand:', ':bride_with_veil:', ':person_with_pouting_face:',
         ':person_frowning:', ':bow:', ':couplekiss:', ':couple_with_heart:', ':massage:', ':haircut:', ':nail_care:', ':boy:',
         ':girl:', ':woman:', ':man:', ':baby:', ':older_woman:', ':older_man:', ':person_with_blond_hair:', ':man_with_gua_pi_mao:',
         ':man_with_turban:', ':construction_worker:', ':cop:', ':angel:', ':princess:', ':smiley_cat:', ':smile_cat:',
         ':heart_eyes_cat:', ':kissing_cat:', ':smirk_cat:', ':scream_cat:', ':crying_cat_face:', ':joy_cat:', ':pouting_cat:',
         ':japanese_ogre:', ':japanese_goblin:', ':see_no_evil:', ':hear_no_evil:', ':speak_no_evil:', ':guardsman:', ':skull:',
         ':feet:', ':lips:', ':kiss:', ':droplet:', ':ear:', ':eyes:', ':nose:', ':tongue:', ':love_letter:', ':bust_in_silhouette:',
         ':busts_in_silhouette:', ':speech_balloon:', ':thought_balloon:', ':feelsgood:', ':finnadie:', ':goberserk:', ':godmode:',
         ':hurtrealbad:', ':rage1:', ':rage2:', ':rage3:', ':rage4:', ':suspect:', ':trollface:', ':sunny:', ':umbrella:', ':cloud:',
         ':snowflake:', ':snowman:', ':zap:', ':cyclone:', ':foggy:', ':ocean:', ':cat:', ':dog:', ':mouse:', ':hamster:', ':rabbit:',
         ':wolf:', ':frog:', ':tiger:', ':koala:', ':bear:', ':pig:', ':pig_nose:', ':cow:', ':boar:', ':monkey_face:', ':monkey:',
         ':horse:', ':racehorse:', ':camel:', ':sheep:', ':elephant:', ':panda_face:', ':snake:', ':bird:', ':baby_chick:',
         ':hatched_chick:', ':hatching_chick:', ':chicken:', ':penguin:', ':turtle:', ':bug:', ':honeybee:', ':ant:', ':beetle:',
         ':snail:', ':octopus:', ':tropical_fish:', ':fish:', ':whale:', ':whale2:', ':dolphin:', ':cow2:', ':ram:', ':rat:',
         ':water_buffalo:', ':tiger2:', ':rabbit2:', ':dragon:', ':goat:', ':rooster:', ':dog2:', ':pig2:', ':mouse2:', ':ox:',
         ':dragon_face:', ':blowfish:', ':crocodile:', ':dromedary_camel:', ':leopard:', ':cat2:', ':poodle:', ':paw_prints:',
         ':bouquet:', ':cherry_blossom:', ':tulip:', ':four_leaf_clover:', ':rose:', ':sunflower:', ':hibiscus:', ':maple_leaf:',
         ':leaves:', ':fallen_leaf:', ':herb:', ':mushroom:', ':cactus:', ':palm_tree:', ':evergreen_tree:', ':deciduous_tree:',
         ':chestnut:', ':seedling:', ':blossom:', ':ear_of_rice:', ':shell:', ':globe_with_meridians:', ':sun_with_face:',
         ':full_moon_with_face:', ':new_moon_with_face:', ':new_moon:', ':waxing_crescent_moon:', ':first_quarter_moon:',
         ':waxing_gibbous_moon:', ':full_moon:', ':waning_gibbous_moon:', ':last_quarter_moon:', ':waning_crescent_moon:',
         ':last_quarter_moon_with_face:', ':first_quarter_moon_with_face:', ':moon:', ':earth_africa:', ':earth_americas:',
         ':earth_asia:', ':volcano:', ':milky_way:', ':partly_sunny:', ':octocat:', ':squirrel:', ':bamboo:', ':gift_heart:',
         ':dolls:', ':school_satchel:', ':mortar_board:', ':flags:', ':fireworks:', ':sparkler:', ':wind_chime:', ':rice_scene:',
         ':jack_o_lantern:', ':ghost:', ':santa:', ':christmas_tree:', ':gift:', ':bell:', ':no_bell:', ':tanabata_tree:', ':tada:',
         ':confetti_ball:', ':balloon:', ':crystal_ball:', ':cd:', ':dvd:', ':floppy_disk:', ':camera:', ':video_camera:',
         ':movie_camera:', ':computer:', ':tv:', ':iphone:', ':phone:', ':telephone:', ':telephone_receiver:', ':pager:', ':fax:',
         ':minidisc:', ':vhs:', ':sound:', ':speaker:', ':mute:', ':loudspeaker:', ':mega:', ':hourglass:', ':hourglass_flowing_sand:',
         ':alarm_clock:', ':watch:', ':radio:', ':satellite:', ':loop:', ':mag:', ':mag_right:', ':unlock:', ':lock:',
         ':lock_with_ink_pen:', ':closed_lock_with_key:', ':key:', ':bulb:', ':flashlight:', ':high_brightness:', ':low_brightness:',
         ':electric_plug:', ':battery:', ':calling:', ':email:', ':mailbox:', ':postbox:', ':bath:', ':bathtub:', ':shower:',
         ':toilet:', ':wrench:', ':nut_and_bolt:', ':hammer:', ':seat:', ':moneybag:', ':yen:', ':dollar:', ':pound:', ':euro:',
         ':credit_card:', ':money_with_wings:', ':e-mail:', ':inbox_tray:', ':outbox_tray:', ':envelope:', ':incoming_envelope:',
         ':postal_horn:', ':mailbox_closed:', ':mailbox_with_mail:', ':mailbox_with_no_mail:', ':package:', ':door:', ':smoking:',
         ':bomb:', ':gun:', ':hocho:', ':pill:', ':syringe:', ':page_facing_up:', ':page_with_curl:', ':bookmark_tabs:', ':bar_chart:',
         ':chart_with_upwards_trend:', ':chart_with_downwards_trend:', ':scroll:', ':clipboard:', ':calendar:', ':date:',
         ':card_index:', ':file_folder:', ':open_file_folder:', ':scissors:', ':pushpin:', ':paperclip:', ':black_nib:', ':pencil2:',
         ':straight_ruler:', ':triangular_ruler:', ':closed_book:', ':green_book:', ':blue_book:', ':orange_book:', ':notebook:',
         ':notebook_with_decorative_cover:', ':ledger:', ':books:', ':bookmark:', ':name_badge:', ':microscope:', ':telescope:',
         ':newspaper:', ':football:', ':basketball:', ':soccer:', ':baseball:', ':tennis:', ':8ball:', ':rugby_football:', ':bowling:',
         ':golf:', ':mountain_bicyclist:', ':bicyclist:', ':horse_racing:', ':snowboarder:', ':swimmer:', ':surfer:', ':ski:',
         ':spades:', ':hearts:', ':clubs:', ':diamonds:', ':gem:', ':ring:', ':trophy:', ':musical_score:', ':musical_keyboard:',
         ':violin:', ':space_invader:', ':video_game:', ':black_joker:', ':flower_playing_cards:', ':game_die:', ':dart:', ':mahjong:',
         ':clapper:', ':memo:', ':pencil:', ':book:', ':art:', ':microphone:', ':headphones:', ':trumpet:', ':saxophone:', ':guitar:',
         ':shoe:', ':sandal:', ':high_heel:', ':lipstick:', ':boot:', ':shirt:', ':tshirt:', ':necktie:', ':womans_clothes:',
         ':dress:', ':running_shirt_with_sash:', ':jeans:', ':kimono:', ':bikini:', ':ribbon:', ':tophat:', ':crown:', ':womans_hat:',
         ':mans_shoe:', ':closed_umbrella:', ':briefcase:', ':handbag:', ':pouch:', ':purse:', ':eyeglasses:',
         ':fishing_pole_and_fish:', ':coffee:', ':tea:', ':sake:', ':baby_bottle:', ':beer:', ':beers:', ':cocktail:',
         ':tropical_drink:', ':wine_glass:', ':fork_and_knife:', ':pizza:', ':hamburger:', ':fries:', ':poultry_leg:',
         ':meat_on_bone:', ':spaghetti:', ':curry:', ':fried_shrimp:', ':bento:', ':sushi:', ':fish_cake:', ':rice_ball:',
         ':rice_cracker:', ':rice:', ':ramen:', ':stew:', ':oden:', ':dango:', ':egg:', ':bread:', ':doughnut:', ':custard:',
         ':icecream:', ':ice_cream:', ':shaved_ice:', ':birthday:', ':cake:', ':cookie:', ':chocolate_bar:', ':candy:', ':lollipop:',
         ':honey_pot:', ':apple:', ':green_apple:', ':tangerine:', ':lemon:', ':cherries:', ':grapes:', ':watermelon:', ':strawberry:',
         ':peach:', ':melon:', ':banana:', ':pear:', ':pineapple:', ':sweet_potato:', ':eggplant:', ':tomato:', ':corn:', 'Places', '',
         ':house:', ':house_with_garden:', ':school:', ':office:', ':post_office:', ':hospital:', ':bank:', ':convenience_store:',
         ':love_hotel:', ':hotel:', ':wedding:', ':church:', ':department_store:', ':european_post_office:', ':city_sunrise:',
         ':city_sunset:', ':japanese_castle:', ':european_castle:', ':tent:', ':factory:', ':tokyo_tower:', ':japan:', ':mount_fuji:',
         ':sunrise_over_mountains:', ':sunrise:', ':stars:', ':statue_of_liberty:', ':bridge_at_night:', ':carousel_horse:',
         ':rainbow:', ':ferris_wheel:', ':fountain:', ':roller_coaster:', ':ship:', ':speedboat:', ':boat:', ':sailboat:', ':rowboat:',
         ':anchor:', ':rocket:', ':airplane:', ':helicopter:', ':steam_locomotive:', ':tram:', ':mountain_railway:', ':bike:',
         ':aerial_tramway:', ':suspension_railway:', ':mountain_cableway:', ':tractor:', ':blue_car:', ':oncoming_automobile:',
         ':car:', ':red_car:', ':taxi:', ':oncoming_taxi:', ':articulated_lorry:', ':bus:', ':oncoming_bus:', ':rotating_light:',
         ':police_car:', ':oncoming_police_car:', ':fire_engine:', ':ambulance:', ':minibus:', ':truck:', ':train:', ':station:',
         ':train2:', ':bullettrain_front:', ':bullettrain_side:', ':light_rail:', ':monorail:', ':railway_car:', ':trolleybus:',
         ':ticket:', ':fuelpump:', ':vertical_traffic_light:', ':traffic_light:', ':warning:', ':construction:', ':beginner:', ':atm:',
         ':slot_machine:', ':busstop:', ':barber:', ':hotsprings:', ':checkered_flag:', ':crossed_flags:', ':izakaya_lantern:',
         ':moyai:', ':circus_tent:', ':performing_arts:', ':round_pushpin:', ':triangular_flag_on_post:', ':jp:', ':kr:', ':cn:',
         ':us:', ':fr:', ':es:', ':it:', ':ru:', ':gb:', ':uk:', ':de:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:',
         ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':1234:', ':zero:', ':hash:', ':symbols:', ':arrow_backward:', ':arrow_down:',
         ':arrow_forward:', ':arrow_left:', ':capital_abcd:', ':abcd:', ':abc:', ':arrow_lower_left:', ':arrow_lower_right:',
         ':arrow_right:', ':arrow_up:', ':arrow_upper_left:', ':arrow_upper_right:', ':arrow_double_down:', ':arrow_double_up:',
         ':arrow_down_small:', ':arrow_heading_down:', ':arrow_heading_up:', ':leftwards_arrow_with_hook:', ':arrow_right_hook:',
         ':left_right_arrow:', ':arrow_up_down:', ':arrow_up_small:', ':arrows_clockwise:', ':arrows_counterclockwise:', ':rewind:',
         ':fast_forward:', ':information_source:', ':ok:', ':twisted_rightwards_arrows:', ':repeat:', ':repeat_one:', ':new:', ':top:',
         ':up:', ':cool:', ':free:', ':ng:', ':cinema:', ':koko:', ':signal_strength:', ':u5272:', ':u5408:', ':u55b6:', ':u6307:',
         ':u6708:', ':u6709:', ':u6e80:', ':u7121:', ':u7533:', ':u7a7a:', ':u7981:', ':sa:', ':restroom:', ':mens:', ':womens:',
         ':baby_symbol:', ':no_smoking:', ':parking:', ':wheelchair:', ':metro:', ':baggage_claim:', ':accept:', ':wc:',
         ':potable_water:', ':put_litter_in_its_place:', ':secret:', ':congratulations:', ':m:', ':passport_control:',
         ':left_luggage:', ':customs:', ':ideograph_advantage:', ':cl:', ':sos:', ':id:', ':no_entry_sign:', ':underage:',
         ':no_mobile_phones:', ':do_not_litter:', ':non-potable_water:', ':no_bicycles:', ':no_pedestrians:', ':children_crossing:',
         ':no_entry:', ':eight_spoked_asterisk:', ':sparkle:', ':eight_pointed_black_star:', ':heart_decoration:', ':vs:',
         ':vibration_mode:', ':mobile_phone_off:', ':chart:', ':currency_exchange:', ':negative_squared_cross_mark:', ':a:', ':b:',
         ':ab:', ':o2:', ':diamond_shape_with_a_dot_inside:', ':recycle:', ':end:', ':back:', ':on:', ':soon:', ':clock1:',
         ':clock130:', ':clock10:', ':clock1030:', ':clock11:', ':clock1130:', ':clock12:', ':clock1230:', ':clock2:', ':clock230:',
         ':clock3:', ':clock330:', ':clock4:', ':clock430:', ':clock5:', ':clock530:', ':clock6:', ':clock630:', ':clock7:',
         ':clock730:', ':clock8:', ':clock830:', ':clock9:', ':clock930:', ':heavy_dollar_sign:', ':copyright:', ':registered:',
         ':tm:', ':x:', ':heavy_exclamation_mark:', ':bangbang:', ':interrobang:', ':o:', ':heavy_multiplication_x:',
         ':heavy_plus_sign:', ':heavy_minus_sign:', ':heavy_division_sign:', ':white_flower:', ':100:', ':heavy_check_mark:',
         ':ballot_box_with_check:', ':radio_button:', ':link:', ':curly_loop:', ':wavy_dash:', ':part_alternation_mark:', ':trident:',
         ':black_small_square:', ':white_small_square:', ':black_medium_small_square:', ':white_medium_small_square:',
         ':black_medium_square:', ':white_medium_square:', ':black_large_square:', ':white_large_square:', ':white_check_mark:',
         ':black_square_button:', ':white_square_button:', ':black_circle:', ':white_circle:', ':red_circle:', ':large_blue_circle:',
         ':large_blue_diamond:', ':large_orange_diamond:', ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:',
         ':small_red_triangle_down:', ':shipit:', ':godmode:']

happyString = ['爽', '好笑', '笑死']
sadString = ['受傷', '難過', '生病', '請假', 'Q_Q', 'QQ']
angryString = ['gogobot*爛']

mMessage = -1
mMessageTime = 0

mReminder = ''

speaker = ''
speak_out = True

lsat_idx = 0




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
    histChecked = []
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
        msg_count = 0

        for msg in message_list:

            msg_len = len(msg)
            if msg_len < 5:
                msg_len = 5

            sleep_time = random.uniform(0, 0.3) * msg_len
            if sleep_time > 9:
                sleep_time = 7 + random.uniform(0, 2)

            # speaking act as sleeping time already, no need to add extra sleep time
            if not speak_out or msg_count == 0:
                time.sleep(sleep_time)

            msg = msg.replace('randname', '@' + random.choice(self.histFrom).replace(' ', ''))
            msg = msg.replace('randmsg', random.choice(self.histMsg))

            self.send(mMessage.getFrom(), msg, message_type=mMessage.getType())

            if self.ShowCompareLog:
                zhprint(' **message "' + msg + '" sended')

            msg_count += 1

            idx = lsat_idx
            while idx < len(self.histMsg):
                self.histChecked[idx] = True
                idx += 1

            # check speaker
            if speak_out and not msg.startswith('http'):
                global speaker

                # detect language
                detected_string_kr1 = re.findall(ur'[\u1100-\u11ff]+', msg)
                detected_string_kr2 = re.findall(ur'[\uac00-\ud7af]+', msg)
                detected_string_jp = re.findall(ur'[\u3040-\u30ff]+', msg)

                if len(speaker) > 0:
                    call(["say", "-v", speaker, msg])
                    print 'speak as custom speaker: ', speaker
                    # reset speaker
                    speaker = ''

                elif len(detected_string_jp) > 0:
                    call(["say", "-v", 'kyoko', msg])
                    print 'speak as japanese'

                elif len(detected_string_kr1) > 0 or len(detected_string_kr2) > 0:
                    call(["say", "-v", 'yuna', msg])
                    print 'speak as korean'

                else:
                    call(["say", msg])
                    print 'speak as default speaker'


    # this thread check schedule and response
    class TimerThread(threading.Thread):

        mChitChat = ''

        def __init__(self, chitchat_self):
            print '** checking thread started **'
            threading.Thread.__init__(self)

            self.mChitChat = chitchat_self

            print 'timer thread started!'


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
                # if (int(time.time()) - mMessageTime) > 3600 * 20 and datetime.datetime.now().hour > 10 \
                # and datetime.datetime.now().hour < 20 and random.randrange(0, 101) < 3 and checkDay('01234'):
                # askMsg = ['吃飯啊', '走了 吃飯啊', '有人要吃東西嗎', '吃飯吃飯吃飯吃飯吃飯', '都沒有人要跟我完', '有人在嗎？？', '幫我開門', '肚子餓了', '大家還在嗎？',
                # '怎麼這麼久都沒有人留言？', '大家好，我是googbot', '都沒人留言 大家都放假去了嗎？', '今天天氣不錯']
                # self.mChitChat.send_from_messages(random.choice(askMsg))

                # global mMessageTime
                # mMessageTime = int(time.time())


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
                            self.mChitChat.send_from_messages(random.choice(r[key_msg]).split('*'))

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
            print 'action LastUpdateTime ', self.LastUpdateTime


    def saveHist(self, message, Msgfrom):

        self.histMsg.append(message)
        self.histFrom.append(Msgfrom)
        self.histChecked.append(False)

        if len(self.histMsg) > MaxHistory:
            self.histMsg.pop(0)
            self.histFrom.pop(0)
            self.histChecked.pop(0)

        if self.ShowTalkHis:
            print '**** printing hist msg ****'
            histMsg = []

            for msg in self.histMsg:
                histMsg.append(msg)
            i = 0
            for name in self.histFrom:
                histMsg[i] = name + ' said:  ' + histMsg[i] + '   status: ' + str(self.histChecked[i])
                i += 1

            for msg in histMsg:
                zhprint(msg)

            print '**** end of hist ****'


    def searchPhoto(self, message_string):

        if (not 'gogobot' in message_string) and (random.random() > 0.2):
            print '**** send search photo FAIL: not for gogobot and random number is less 0.2 ****'
            return False

        q = { 'v' : '1.0', 'q' : message_string.replace("gogobot", "").replace("@", "").replace(": ", "")}
        print '**** search photo url: ' + 'https://ajax.googleapis.com/ajax/services/search/images?' + urllib.urlencode(q) + ' ****'
        responseData = json.loads(requests.get('https://ajax.googleapis.com/ajax/services/search/images?' + urllib.urlencode(q)).content)
        
        if not responseData:
            print '**** send search photo FAIL: responseData == null ****'
            return False

        length = len(responseData['responseData']['results'])

        if length == 0:
            print '**** send search photo FAIL: length == 0 ****'
            return False

        index = int(random.random() * length)
        photo = responseData['responseData']['results'][index]['url']
        if photo:
            print '**** send search photo: ' + photo + ' ****'
            self.send_from_messages([photo])
            return True
        else:
            print '**** send search photo FAIL: photo == null ****'
            return False


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

            if self.checkIfContain([u'天氣', u'氣溫']):
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
            self.send(mMessage.getFrom(), random.choice(rainNoti), message_type=mMessage.getType())


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
        self.send(mMessage.getFrom(), msg, message_type=mMessage.getType())

        if u"雨" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"多雲" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"晴" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] and (
                    int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@duo大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(mMessage.getFrom(), random.choice(rainNoti), message_type=mMessage.getType())


    # change status of speak function
    def check_modify_speak_status(self, msg):

        if not 'gogobot' in msg:
            return False

        activate_strings = ['開啟語音', '不要念']
        deactivate_strings = ['關閉語音', '念出來']

        for astring in activate_strings:
            if astring in msg:
                global speak_out
                speak_out = True
                print 'speak is turn on for keyword: ', astring
                return True

        for dstring in deactivate_strings:
            if dstring in msg:
                global speak_out
                speak_out = False
                print 'speak is turn off for keyword: ', dstring
                return True

        return False


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

                self.send_from_messages(response_messages)
                print' **random message "', response_messages, '" sended'

            else:
                if random.randrange(0, 101) > 50:
                    radReply = ['http://i.imgur.com/DJG1aF4.jpg', 'http://i.imgur.com/ggvWFBo.jpg', 'http://i.imgur.com/xovuE25.jpg',
                                'http://i.imgur.com/uSGbEFG.jpg', 'http://i.imgur.com/mAuzhW9.jpg', 'http://i.imgur.com/8J0DPac.jpg',
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg)]

                    response_messages = random.choice(radReply).split('*')

                    self.send_from_messages([response_messages])

                else:
                    msg = random.choice(emoji)
                    self.send_from_messages([msg])
                    print' **random message "', msg, '" sended'

            return True

        return False


    # def antiWash(self):
    # return False
    #
    # # remove antiwash function
    #
    # if len(self.histFrom) - self.histPisiton < 7:
    # return False
    #
    # samePerson = True
    # firstPesron = self.histFrom[self.histPisiton]
    #
    # i = self.histPisiton
    # while i > 0 and i > self.histPisiton - 7:
    # if firstPesron != self.histFrom[i]:
    # print 'name', self.histFrom[i]
    # samePerson = False
    # i -= 1
    # break
    #
    # if samePerson:
    # if random.randrange(0, 101) > 75:
    # self.angry += 3
    # response = ['可以不要洗版了嗎？', '洗版很好玩嗎？', '不要為了要我回文亂發言好嗎？', '人的忍耐是有限度的！']
    #             self.send(mMessage.getFrom(), random.choice(response), message_type=mMessage.getType())
    #         else:
    #             if random.randrange(0, 101) > 80:
    #                 self.angry += 2
    #                 self.happy += 3
    #                 i = 0
    #                 for msg in self.histMsg:
    #                     self.send(mMessage.getFrom(), random.choice(self.histMsg), message_type=mMessage.getType())
    #                     i += 1
    #                     if i > 7:
    #                         return True
    #
    #     return samePerson


    def printCurrentEmotion(self):
        print '*** print emo ***'
        print 'happy: ', self.happy, 'sad: ', self.sad, 'angry level: ', self.angry
        print'*** lastCheckTime: ', self.lastCheckTime, ' ***'


    def checkIfContain(self, keyArray):
        # total key array
        for key in keyArray:
            keyArray_ = key.split('*')

            # is this a key for 'gogobot personal chat'?
            is_gogobot_key = False

            for key_ in keyArray_:
                if key_.lower() == 'gogobot':
                    is_gogobot_key = True

            message = ''
            idx = len(self.histMsg)

            if is_gogobot_key:


                print str(idx - 1 >= 0), '!!!!', str((len(self.histMsg) - 1) - idx <= MaxComprehensiveLine)

                while idx - 1 >= 0 and (len(self.histMsg) - 1) - idx <= MaxComprehensiveLine:
                    idx -= 1
                    print 'current idx: ', idx, '  msg: ', self.histMsg[idx], 'isChecked: ', self.histChecked[idx]

                    if self.histChecked[idx] == False or (len(self.histMsg[idx]) < 10 and 'gogobot' in self.histMsg[idx].lower()):
                        message = message + self.histMsg[idx]

                print 'appended message: ', message

            else:
                message = self.histMsg[len(self.histMsg) - 1]

            match_key = True

            for key_ in keyArray_:
                if key_ not in message:
                    match_key = False

            if match_key:
                global lsat_idx
                lsat_idx = idx

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
        if self.checkIfContain(happyString):
            if self.ShowEmoLog:
                print 'happy str matched: ' + message_string
            self.happy += 1

        if self.checkIfContain(sadString):
            if self.ShowEmoLog:
                print 'sad str matched: ' + message_string
            self.sad += 1

        if self.checkIfContain(angryString):
            if self.ShowEmoLog:
                print 'angry str matched: ' + message_string
            self.angry += 1


    def checkGogobotCmd(self, message):
        # reload all action list
        if 'gogoreload' in message:
            print 'COMMDAND RECEIVED: reload action list'
            self.LastUpdateTime = 0
            self.send(mMessage.getFrom(), 'command received, reloading', message_type=mMessage.getType())

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

        # if 'gogowash' in message:
        #     if self.ShowAntiWash:
        #         self.ShowAntiWash = False
        #     else:
        #         self.ShowAntiWash = True
        #
        #     self.send(mMessage.getFrom(), 'antiwash status is now :' + self.ShowAntiWash, message_type=mMessage.getType())
        #     print 'COMMDAND RECEIVED: antiwash status is now :', self.ShowAntiWash

        if 'gogoremindlog' in message:

            if self.show_reminder_log:
                self.show_reminder_log = False
            else:
                self.show_reminder_log = True
            self.send(mMessage.getFrom(), 'gogoremindlog status is now :' + self.show_reminder_log,
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

        if not message_from or not message_string:
            print 'error ', message_from
            print 'error ', message_string
            return

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




        # random response #1
        if self.checkSendRandomMessage():
            return

        if self.check_modify_speak_status(message_string):
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

        # if self.ShowAntiWash and self.antiWash():
        #     return

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

            if self.checkIfContain(action['keyword']):
                if self.ShowCompareLog:
                    print '"', action['keyword'][0], '" matched'

                if 'chance' in action:
                    if self.ShowCompareLog:
                        zhprint(' ** ' + ''.join(action['keyword']) + ' has roll-key, have to roll ')
                    if random.randrange(0, 101) < int(action['chance']):
                        if self.ShowCompareLog:
                            print ' **rand < ', action['chance'], ', roll success!!'
                        totalMessage = random.choice(action['response'])
                        response_messages = totalMessage.split('*')

                        self.send_from_messages(response_messages)
                        self.histChecked[len(self.histChecked) - 1] = True

                        # print 'set ',len(self.histChecked)-1 , 'to True'

                        return
                    elif self.ShowCompareLog:
                        print ' **rand > ', action['chance'], ', roll failed!'

                else:
                    totalMessage = random.choice(action['response'])
                    response_messages = totalMessage.split('*')

                    self.send_from_messages(response_messages)
                    self.histChecked[len(self.histChecked) - 1] = True

                    # print 'set ',len(self.histChecked)-1 , 'to True'

                    return


        if self.searchPhoto(message_string):
            return

        # random response #2
        if self.checkSendRandomMessage():
            return

        if self.ShowCompareLog and counter != 0:
            print 'chceck keyword: ', Appendedkeyword

        print '****** end checking action *****'

