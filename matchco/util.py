from itertools import combinations, chain


def subsequences(txt, minlength=3):
   "generate all ordered multi-term (split by whitespace) text subsequences"

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
