# encoding: utf-8

import re
from itertools import combinations, chain
try:
    from future_builtins import filter
except ImportError:
    pass

from cleanco import basename

normlz_dashs = re.compile("\ *-\ *")
normlz_dots = re.compile("\ *\.\ *")


def normalized(name, umlauts=False):
   "normalize the name"

   # remove legal terms & extra whitespace & other trash
   name = basename(name)

   # lowercase
   name = name.lower()

   # optionally convert umlauts
   if umlauts:
      name = name.replace(u'ä',u'a').replace(u'ö',u'o').replace(u'å',u'a')

   # normalize dots and dashes
   name = re.sub(normlz_dashs,'-', name)
   name = re.sub(normlz_dots,'.', name)

   return name


def subsequences(txt, minlength=3, normalize=None):
   "generate all ordered multi-term (split by whitespace) text subsequences"

   #assert type(txt) == unicode
   if normalize:
      txt = normalize(txt)

   # whitespace - separated parts
   parts = txt.split()
   subs = []
   for l in reversed(range(1, len(parts)+1)):
      subs.extend([' '.join(ss) for ss in combinations(parts, l) if ' '.join(ss) in txt])
   ws_separated = set([s for s in subs if len(s) >= minlength])

   # augment parts with dash & dot separation
   dashsplit = [s.split('-') for s in ws_separated]
   dashcombo = [[s.replace('-','') for s in ws_separated if '-' in s]]
   dotsplit = [s.split('.') for s in ws_separated]

   def tokenfilter(token, existing=ws_separated, minlength=minlength):
      "filter out tokens by e.g. min length or other requirement(s)"
      return True if len(token) >= minlength else False

   extras = filter(tokenfilter, chain.from_iterable((dashsplit + dashcombo + dotsplit)))
   return list(ws_separated.union(extras))

