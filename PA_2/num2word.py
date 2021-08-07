#based on pip num2words
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

import math
from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal

#currency
def parse_currency_parts(value, is_int_with_cents=True):
    if isinstance(value, int):
        if is_int_with_cents:
            # assume cents if value is integer
            negative = value < 0
            value = abs(value)
            integer, cents = divmod(value, 100)
        else:
            negative = value < 0
            integer, cents = abs(value), 0
    else:
        value = Decimal(value)
        value = value.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
        negative = value < 0
        value = abs(value)
        integer, fraction = divmod(value, 1)
        integer = int(integer)
        cents = int(fraction * 100)

    return integer, cents, negative

def prefix_currency(prefix, base):
    return tuple("%s %s" % (prefix, i) for i in base)

#compat
def to_s(val):
    return str(val)

#base

class Num2Word_Base(object):
    CURRENCY_FORMS = {}
    CURRENCY_ADJECTIVES = {}

    def __init__(self):
        self.is_title = False
        self.precision = 2
        self.exclude_title = []
        self.negword = "(-) "
        self.pointword = "(.)"
        self.errmsg_nonnum = "type(%s) not in [long, int, float]"
        self.errmsg_floatord = "Cannot treat float %s as ordinal."
        self.errmsg_negord = "Cannot treat negative num %s as ordinal."
        self.errmsg_toobig = "abs(%s) must be less than %s."

        self.setup()

        # uses cards
        if any(hasattr(self, field) for field in ['high_numwords', 'mid_numwords', 'low_numwords']):
            self.cards = OrderedDict()
            self.set_numwords()
            self.MAXVAL = 1000 * list(self.cards.keys())[0]

    def set_numwords(self):
        self.set_high_numwords(self.high_numwords)
        self.set_mid_numwords(self.mid_numwords)
        self.set_low_numwords(self.low_numwords)

    def set_high_numwords(self, *args):
        raise NotImplementedError

    def set_mid_numwords(self, mid):
        for key, val in mid:
            self.cards[key] = val

    def set_low_numwords(self, numwords):
        for word, n in zip(numwords, range(len(numwords) - 1, -1, -1)):
            self.cards[n] = word

    def splitnum(self, value):
        for elem in self.cards:
            if elem > value:
                continue

            out = []
            if value == 0:
                div, mod = 1, 0
            else:
                div, mod = divmod(value, elem)

            if div == 1:
                out.append((self.cards[1], 1))
            else:
                if div == value:  # The system tallies, eg Roman Numerals
                    return [(div * self.cards[elem], div*elem)]
                out.append(self.splitnum(div))

            out.append((self.cards[elem], elem))

            if mod:
                out.append(self.splitnum(mod))

            return out

    def parse_minus(self, num_str):
        """Detach minus and return it as symbol with new num_str."""
        if num_str.startswith('-'):
            # Extra spacing to compensate if there is no minus.
            return '%s ' % self.negword, num_str[1:]
        return '', num_str

    def str_to_number(self, value):
        return Decimal(value)

    def to_cardinal(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        out = ""
        if value < 0:
            value = abs(value)
            out = self.negword

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        val = self.splitnum(value)
        words, num = self.clean(val)
        return self.title(out + words)

    def float2tuple(self, value):
        pre = int(value)

        # Simple way of finding decimal places to update the precision
        self.precision = abs(Decimal(str(value)).as_tuple().exponent)

        post = abs(value - pre) * 10**self.precision
        if abs(round(post) - post) < 0.01:
            post = int(round(post))
        else:
            post = int(math.floor(post))

        return pre, post

    def to_cardinal_float(self, value):
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError, AttributeError):
            raise TypeError(self.errmsg_nonnum % value)

        pre, post = self.float2tuple(float(value))

        post = str(post)
        post = '0' * (self.precision - len(post)) + post

        out = [self.to_cardinal(pre)]
        if self.precision:
            out.append(self.title(self.pointword))

        for i in range(self.precision):
            curr = int(post[i])
            out.append(to_s(self.to_cardinal(curr)))

        return " ".join(out)

    def merge(self, curr, next):
        raise NotImplementedError

    def clean(self, val):
        out = val
        while len(val) != 1:
            out = []
            left, right = val[:2]
            if isinstance(left, tuple) and isinstance(right, tuple):
                out.append(self.merge(left, right))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]

    def title(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])
            value = " ".join(out)
        return value

    def verify_ordinal(self, value):
        if not value == int(value):
            raise TypeError(self.errmsg_floatord % value)
        if not abs(value) == value:
            raise TypeError(self.errmsg_negord % value)

    def to_ordinal(self, value):
        return self.to_cardinal(value)

    def to_ordinal_num(self, value):
        return value

    # Trivial version
    def inflect(self, value, text):
        text = text.split("/")
        if value == 1:
            return text[0]
        return "".join(text)

    # //CHECK: generalise? Any others like pounds/shillings/pence?
    def to_splitnum(self, val, hightxt="", lowtxt="", jointxt="", divisor=100, longval=True, cents=True):
        out = []
        if isinstance(val, float):
            high, low = self.float2tuple(val)
        else:
            try:
                high, low = val
            except TypeError:
                high, low = divmod(val, divisor)

        if high:
            hightxt = self.title(self.inflect(high, hightxt))
            out.append(self.to_cardinal(high))
            if low:
                if longval:
                    if hightxt:
                        out.append(hightxt)
                    if jointxt:
                        out.append(self.title(jointxt))
            elif hightxt:
                out.append(hightxt)

        if low:
            if cents:
                out.append(self.to_cardinal(low))
            else:
                out.append("%02d" % low)
            if lowtxt and longval:
                out.append(self.title(self.inflect(low, lowtxt)))

        return " ".join(out)

    def to_year(self, value, **kwargs):
        return self.to_cardinal(value)

    def pluralize(self, n, forms):
        raise NotImplementedError

    def _money_verbose(self, number, currency):
        return self.to_cardinal(number)

    def _cents_verbose(self, number, currency):
        return self.to_cardinal(number)

    def _cents_terse(self, number, currency):
        return "%02d" % number

    def to_currency(self, val, currency='EUR', cents=True, separator=',', adjective=False):
        """
        Args:
            val: Numeric value
            currency (str): Currency code
            cents (bool): Verbose cents
            separator (str): Cent separator
            adjective (bool): Prefix currency name with adjective
        Returns:
            str: Formatted string

        """
        left, right, is_negative = parse_currency_parts(val)

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]

        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"' %
                (currency, self.__class__.__name__))

        if adjective and currency in self.CURRENCY_ADJECTIVES:
            cr1 = prefix_currency(self.CURRENCY_ADJECTIVES[currency], cr1)

        minus_str = "%s " % self.negword if is_negative else ""
        money_str = self._money_verbose(left, currency)
        cents_str = self._cents_verbose(right, currency) if cents else self._cents_terse(right, currency)

        return u'%s%s %s%s %s %s' % (minus_str, money_str, self.pluralize(left, cr1), separator, cents_str, self.pluralize(right, cr2))

    def setup(self):
        pass

# lang EU

class Num2Word_EU(Num2Word_Base):
    
    GENERIC_DOLLARS = ('dollar', 'dollars')
    GENERIC_CENTS = ('cent', 'cents')

    CURRENCY_FORMS = { 'AUD': (GENERIC_DOLLARS, GENERIC_CENTS), 'CAD': (GENERIC_DOLLARS, GENERIC_CENTS),
        # repalced by EUR
        'EEK': (('kroon', 'kroons'), ('sent', 'senti')), 'EUR': (('euro', 'euro'), GENERIC_CENTS),
        'GBP': (('pound sterling', 'pounds sterling'), ('penny', 'pence')), 'LTL': (('litas', 'litas'), GENERIC_CENTS),
        # replaced by EUR
        'LVL': (('lat', 'lats'), ('santim', 'santims')), 'USD': (GENERIC_DOLLARS, GENERIC_CENTS),
        'RUB': (('rouble', 'roubles'), ('kopek', 'kopeks')), 'SEK': (('krona', 'kronor'), ('öre', 'öre')),
        'NOK': (('krone', 'kroner'), ('øre', 'øre')), 'PLN': (('zloty', 'zlotys', 'zlotu'), ('grosz', 'groszy')),
        'MXN': (('peso', 'pesos'), GENERIC_CENTS), 'RON': (('leu', 'lei', 'de lei'), ('ban', 'bani', 'de bani')),
        'INR': (('rupee', 'rupees'), ('paisa', 'paise')), 'HUF': (('forint', 'forint'), ('fillér', 'fillér'))
    }

    CURRENCY_ADJECTIVES = {'AUD': 'Australian', 'CAD': 'Canadian', 'EEK': 'Estonian', 'USD': 'US',
        'RUB': 'Russian', 'NOK': 'Norwegian', 'MXN': 'Mexican', 'RON': 'Romanian', 'INR': 'Indian', 'HUF': 'Hungarian'}

    GIGA_SUFFIX = "illiard"
    MEGA_SUFFIX = "illion"

    def set_high_numwords(self, high):
        cap = 3 + 6 * len(high)

        for word, n in zip(high, range(cap, 3, -6)):
            if self.GIGA_SUFFIX:
                self.cards[10 ** n] = word + self.GIGA_SUFFIX

            if self.MEGA_SUFFIX:
                self.cards[10 ** (n - 3)] = word + self.MEGA_SUFFIX

    def gen_high_numwords(self, units, tens, lows):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def pluralize(self, n, forms):
        form = 0 if n == 1 else 1
        return forms[form]

    def setup(self):
        lows = ["non", "oct", "sept", "sext", "quint", "quadr", "tr", "b", "m"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept", "octo", "novem"]
        tens = ["dec", "vigint", "trigint", "quadragint", "quinquagint", "sexagint", "septuagint", "octogint", "nonagint"]
        self.high_numwords = ["cent"] + self.gen_high_numwords(units, tens, lows)

# lang EN

class Num2Word_EN(Num2Word_EU):
    def set_high_numwords(self, high):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word + "illion"

    def setup(self):
        super(Num2Word_EN, self).setup()

        self.negword = "minus "
        self.pointword = "point"
        self.exclude_title = ["and", "point", "minus"]

        self.mid_numwords = [(1000, "thousand"), (100, "hundred"), (90, "ninety"), (80, "eighty"), (70, "seventy"),
                             (60, "sixty"), (50, "fifty"), (40, "forty"),(30, "thirty")]
        self.low_numwords = ["twenty", "nineteen", "eighteen", "seventeen", "sixteen", "fifteen", "fourteen", "thirteen",
                             "twelve", "eleven", "ten", "nine", "eight", "seven", "six", "five", "four", "three", "two",
                             "one", "zero"]
        self.ords = {"one": "first", "two": "second", "three": "third", "four": "fourth", "five": "fifth", "six": "sixth",
        "seven": "seventh", "eight": "eighth", "nine": "ninth", "ten": "tenth", "eleven": "eleventh", "twelve": "twelfth"}

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s-%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s and %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s, %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == "y":
                lastword = lastword[:-1] + "ie"
            lastword += "th"
        lastwords[-1] = self.title(lastword)
        outwords[-1] = "-".join(lastwords)
        return " ".join(outwords)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s" % (value, self.to_ordinal(value)[-2:])

    def to_year(self, val, suffix=None, longval=True):
        if val < 0:
            val = abs(val)
            suffix = 'BC' if not suffix else suffix
        high, low = (val // 100, val % 100)
        # If year is 00XX, X00X, or beyond 9999, go cardinal.
        if (high == 0
                or (high % 10 == 0 and low < 10)
                or high >= 100):
            valtext = self.to_cardinal(val)
        else:
            hightext = self.to_cardinal(high)
            if low == 0:
                lowtext = "hundred"
            elif low < 10:
                lowtext = "oh-%s" % self.to_cardinal(low)
            else:
                lowtext = self.to_cardinal(low)
            valtext = "%s %s" % (hightext, lowtext)
        return (valtext if not suffix
                else "%s %s" % (valtext, suffix))




CONVERTES_TYPES = ['cardinal', 'ordinal', 'ordinal_num', 'year', 'currency']

def num2words(number, ordinal=False, to='cardinal', **kwargs):
    '''
        Converts a number to word. Only avail in english
        CONVERTER_CLASSES = {'en': Num2Word_EN()}
    '''
    converter = Num2Word_EN()

    if isinstance(number, str):
        number = converter.str_to_number(number)

    # backwards compatible
    if ordinal:
        return converter.to_ordinal(number)

    if to not in CONVERTES_TYPES:
        raise NotImplementedError()

    return getattr(converter, 'to_{}'.format(to))(number, **kwargs)

if __name__ == '__main__':
    print(num2words(number='2', ordinal=True, to='ordinal'))
