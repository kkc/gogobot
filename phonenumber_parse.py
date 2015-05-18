#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import phonenumbers
import re


class ExtendCarrier():
    carrier_tw = {
        '886908': u"台灣之星門號", '886905': u"中華門號",
        '886909': u"台哥大門號", '886903': u"遠傳門號"}

    def get_extend_carrier(self, number, region):

        if region == 'TW':
            return self.carrier_tw.get(number[0:6], '')
        else:
            return ''

extend_carrier = ExtendCarrier()


class PhonenumberParse(object):

    def __eq__(self, other):
        return self.__numobj == other.numobj and  \
            self.__number == other.number and  \
            self.__e164 == other.e164 and  \
            self.__region == other.region

    def __init__(self, number, region='ERROR'):
        # number : e164 or local number
        # init value
        self.__numobj = None
        self.__number = ''  # 目前 whoscall 使用的 ex:886223686999
        self.__e164 = ''  # 號碼本身 ex:+886223686999
        self.__region = 'ERROR'  # TW
        self.__type = ''
        self.__internation = ''
        self.__national = ''
        self.__national_digital = ''

        # set value
        number = re.sub(r'[^0123456789+*#]', '', number)
        self.__number = number
        self.__e164 = number

        if region and (region in phonenumbers.SUPPORTED_REGIONS or region in phonenumbers.REGION_CODE_FOR_NON_GEO_ENTITY):
            region = region.upper()
        else:
            region = 'ERROR'

        self.__region = region

        is_parse = False

        if not (number.startswith('*') or number.startswith('#')):
            try:
                self.__numobj = phonenumbers.parse(
                    self.__number, self.__region)

                if phonenumbers.is_possible_number(self.__numobj):
                    is_parse = True

            except phonenumbers.NumberParseException as e:
                pass

        if is_parse:
            self.__e164 = phonenumbers.format_number(
                self.__numobj, phonenumbers.PhoneNumberFormat.E164)
            self.__number = self.__e164[1:]

            temp_region = phonenumbers.region_code_for_number(self.__numobj)

            if temp_region is None:
                temp_region = region
            self.__region = temp_region.upper()

        else:
            self.__e164 = number
            self.__number = number
            self.__region = region
            self.__numobj = None

        self.__e164 = self.__e164[:257]
        self.__number = self.__number[:256]

    @property
    def numobj(self):
        return self.__numobj

    @property
    def number(self):
        return self.__number

    @property
    def e164(self):
        return self.__e164

    @property
    def region(self):
        return self.__region

    @property
    def region(self):
        return self.__region

    @property
    def type(self):
        if self.__type == '':
            if self.__numobj:
                self.__type = phonenumbers.number_type(self.__numobj)

        return self.__type

    @property
    def is_fixed_number(self):
        return self.type == phonenumbers.PhoneNumberType.FIXED_LINE

    @property
    def is_valid_number(self):
        if self.__numobj:
            return phonenumbers.is_valid_number(self.__numobj)

        else:
            return False

    @property
    def is_possible_number(self):
        if self.__numobj:
            return phonenumbers.is_possible_number(self.__numobj)

        else:
            return False

    @property
    def internation(self):
        if self.__internation == '':
            self.__internation = self._get_internation()

        return self.__internation

    @property
    def national(self):
        if self.__national == '':
            self.__national = self._get_national()
        return self.__national

    @property
    def nationaldigital(self):
        if self.__national_digital == '':
            self.__national_digital = self._get_national_digital()
        return self.__national_digital

    def get_country_code(self):
        country_code = None

        if not self.__numobj:
            return country_code

        country_code = phonenumbers.country_code_for_region(
            self.__region)

        return country_code

    def _get_internation(self):

        internation_num = self.__number

        if not self.__numobj:
            return internation_num

        internation_num = phonenumbers.format_number(
            self.__numobj,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL).replace("+", "")

        return internation_num

    def _get_national(self):
        national_num = self.__number

        if not self.__numobj:
            return national_num

        national_num = phonenumbers.format_number(
            self.__numobj, phonenumbers.PhoneNumberFormat.NATIONAL)

        return national_num

    def _get_national_digital(self):
        return re.sub(r'\D', "", self.national)

    def get_geocoding(self, language="en", accept_language=''):
        geocoding = ''

        if not self.__numobj:
            return geocoding

        from phonenumbers.geocoder import description_for_number
        if len(accept_language) > 0:
            geocoding = str(description_for_number(
                self.__numobj, accept_language.split(";")[0]).encode("utf-8"))

        if len(geocoding) == 0:
            geocoding = str(description_for_number(
                self.__numobj, language).encode("utf-8"))

        if len(geocoding) == 0 and self.__number.startswith("8869"):
            if accept_language != '' and accept_language.find("zh") > -1:
                geocoding = u"台灣"

            else:
                geocoding = "Taiwan"

        return geocoding

    def get_carrier(self, language="EN"):

        carrier_name = ''

        if self.region == '001':

            if self.number.startswith('870') or self.number.startswith('881') or self.number.startswith('882'):
                return u'衛星電話'

        if self.__region == 'TW':
            carrier_name = extend_carrier.get_extend_carrier(
                self.__number, self.__region)

        if carrier_name == '' and self.__numobj:
            from phonenumbers import carrier
            carrier_name = carrier.name_for_number(self.__numobj, language)

        return carrier_name

    def get_googleformat(self):
        formatstring = ''
        internation_num = self.internation
        national_num = self.national
        national_digital_num = self.nationaldigital

        if not self.__numobj:
            formatstring = internation_num
            return formatstring

        formatstring = formatstring + "\"" + internation_num + "\""
        formatstring = formatstring + " OR "
        formatstring = formatstring + "\"" + self.__number + "\""
        formatstring = formatstring + " OR "
        formatstring = formatstring + "\"" + national_num + "\""
        formatstring = formatstring + " OR "
        formatstring = formatstring + "\"" + national_digital_num + "\""

        if self.__region == "TW":
            nationlist = national_num.rsplit(" ")

            if len(nationlist) == 3:
                formatstring = formatstring + " OR "
                formatstring = formatstring + "\"" + \
                    nationlist[0] + " " + nationlist[1] + nationlist[2] + "\""

            if self.__number[:5] in ["88637", "88689", "88649"]:
                formatstring = formatstring + " OR "
                formatstring = formatstring + "\"" + self.__number[:3] + " " + self.__number[
                    3:5] + " " + self.__number[5:8] + " " + self.__number[8:] + "\""
                formatstring = formatstring + " OR "
                formatstring = formatstring + "\"" + \
                    national_digital_num[
                        :3] + " " + national_digital_num[3:6] + " " + national_digital_num[6:] + "\""
                formatstring = formatstring + " OR "
                formatstring = formatstring + "\"" + \
                    national_digital_num[:3] + " " + \
                    national_digital_num[3:] + "\""

        elif self.__region == "VN":
            internationlist = internation_num.rsplit(" ")

            if len(internationlist) == 4:
                formatstring = formatstring + " OR "
                formatstring = formatstring + "\"" + \
                    internationlist[0] + " " + internationlist[1] + \
                    " " + internationlist[2] + internationlist[3] + "\""

        elif self.__region == "JP":
            nationlist = national_num.rsplit("-")

            if len(nationlist) >= 2 and len(nationlist[0]) > 2:
                format_433 = True
                format_334 = True
                format_424 = True

                if len(nationlist[0]) == 3 and len(nationlist[1]) == 3:
                    format_334 = False
                elif len(nationlist[0]) == 4 and len(nationlist[1]) == 3:
                    format_433 = False
                elif len(nationlist[0]) == 4 and len(nationlist[1]) == 2:
                    format_424 = False

                if format_433:
                    formatstring = formatstring + " OR "
                    formatstring = formatstring + "\"" + \
                        national_digital_num[
                            0:4] + "-" + national_digital_num[4:7] + "-" + national_digital_num[7:] + "\""
                if format_334:
                    formatstring = formatstring + " OR "
                    formatstring = formatstring + "\"" + \
                        national_digital_num[
                            0:3] + "-" + national_digital_num[3:6] + "-" + national_digital_num[6:] + "\""
                if format_424:
                    formatstring = formatstring + " OR "
                    formatstring = formatstring + "\"" + \
                        national_digital_num[
                            0:4] + "-" + national_digital_num[4:6] + "-" + national_digital_num[6:] + "\""

        return formatstring

    def get_SG_format(self):
        ''' should return list '''
        country_code = self.get_country_code()
        national_num = self.national
        format_string = "+" + country_code + \
            " " + national_num.replace(" ", "-")

        return [format_string]

    def get_HK_format(self):
        ''' should return list '''
        national_num = self.national
        format_string = national_num.replace(" ", "-")
        return [format_string]

    def get_AU_format(self):
        ''' should return list '''
        format_list = []
        national_num = self.national
        nation_list = national_num.split(" ")

        if len(nation_list) >= 3:
            format_list.append(
                "(" + nation_list[0] + ") " + nation_list[1] + " " + nation_list[2])

        return format_list

    def get_TH_format(self):
        ''' should return list

            number format :02-890-8755
                           038-421-707
        '''
        format_list = []
        national_num = self.national
        nation_list = national_num.split(" ")

        if len(nation_list) >= 3:
            format_list.append(
                nation_list[0] + "-" + nation_list[1] + "-" + nation_list[2])

        return format_list

    def get_MY_format(self):
        ''' should return list

            number format: 03 8011 8033
                           +60167799936
                           016-3307255
                           0127700827
        '''
        format_list = []
        format_list.append(self.__e164)
        format_list.append(self.__number)
        format_list.append(self.__number.replace('- ', ''))
        national_num = self.national
        internation_num = self.internation

        nation_list = national_num.split(" ")  # 016-330 7255
        if len(nation_list) >= 2:
            format_list.append("+" + nation_list[0] + " " + nation_list[1])
            format_list.append(nation_list[0] + nation_list[1])

        international = internation_num.split(" ")
        if len(international) >= 3:
            format_list.append(
                international[0] + international[1] + " " + international[2])

        return format_list

    def get_SE_format(self):
        ''' should return list '''
        format_list = []
        national_num = self.national
        nation_list = national_num.split("-")
        if len(nation_list) >= 2:
            format_list.append(
                "(" + nation_list[0] + ") " + nation_list[1].replace(" ", ""))

        return format_list

    def get_ID_format(self):
        ''' should return list

            format: (021) 797 6569
                    (021) 7278 1100
        '''
        format_list = []
        national_num = self.national
        nation_list = national_num.split(" ")  # (021) 7976569
        if len(nation_list) >= 2:
            if len(nation_list[1]) == 7:
                format_list.append(
                    nation_list[0] + " " + nation_list[1][0:3] + " " + nation_list[1][3:7])
            elif len(nation_list[1]) == 8:
                format_list.append(
                    nation_list[0] + " " + nation_list[1][0:4] + " " + nation_list[1][4:8])

        return format_list

    def get_factualformat(self):
        formatstring = []
        national_num = self.national
        internation_num = self.internation
        national_digital_num = self.nationaldigital

        if not self.__numobj:
            formatstring.append(internation_num)
            return formatstring

        formatstring.append(internation_num)       # 886 2 2368 6999
        formatstring.append(self.__number)              # 886223686999
        formatstring.append(national_num)          # 02 2368 6999
        formatstring.append(national_digital_num)   # 0223686999

        if national_num.startswith("0"):
            formatstring.append(national_num[1:])  # 2 2368 6999
            formatstring.append(national_digital_num[1:])  # 223686999
            formatstring.append(national_digital_num[:2] +
                                "-" + national_digital_num[2:])  # 02-23686999
        formatstring.append("+" + internation_num)  # +886 2 2368 6999
        formatstring.append("+" + self.__number)         # +886223686999

        format_mapping = {
            'SG': self.get_SG_format,
            'HK': self.get_HK_format,
            'AU': self.get_AU_format,
            'SE': self.get_SE_format,
            'TH': self.get_TH_format,
            'MY': self.get_MY_format,
            'ID': self.get_ID_format,
        }
        if self.__region in format_mapping:
            number_format = format_mapping[self.__region]()
            formatstring.extend(number_format)

        return formatstring
