# encoding: utf-8

from distance import jaccard, nlevenshtein, sorensen
from jellyfish import damerau_levenshtein_distance as damerau
from .algorithms import sift4


def closestvariation(term, variations, method):
   "determine how close we get to a normalized term with a set of variations, at best"

   assert type(term) == str, "term to find closest name variation for must be str"
   assert variations, "need name variations to compare against, not just an empty list"

   method = method.lower().strip() # just in case

   if method == "jaccard":
      results = {v:jaccard(term, v) for v in variations}
   elif method == "levenshtein":
      results = {v:nlevenshtein(term, v) for v in variations}
   elif method == "damerau":
      results = {v:damerau(term, v)*1.0/ max(len(term),len(v))*1.0 for v in variations}
   elif method == "sorensen":
      results = {v:sorensen(term, v) for v in variations}
   elif method == "sift":
      results = {v:sift4(term, v)/ max(len(term),len(v)*1.0) for v in variations}
   else:
      raise Exception("unknown method: '%s'" % method)

   topcertainty = min(results.values())

   # return best variation and its level of certainty
   swapped = dict(zip(results.values(),results))
   return (swapped[topcertainty], topcertainty)


class NoMatchError(Exception):
   "raised when matchco finds no match within threshold"

   def __init__(self, msg, term, certainty, closest):
      Exception.__init__(self, msg)
      self.term = term
      self.certainty = certainty
      self.closest = closest


class AmbiguousMatchError(Exception):
   "raised when matchco gets multiple equally good matches"

   def __init__(self, msg, term, certainty, matches):
      Exception.__init__(self, msg)
      self.term = term
      self.certainty = certainty
      self.matches = matches


def bestmatch(txt, candidate_data, maxdiff=0.29, method="damerau", multiple=False, matchlen=True):
   "return best matching candidate and the variation that produced the match"

   assert type(txt) == str, "%s is not str, change it" % str(txt)
   txt = txt.lower()

   results = {}
   for candidate, normalized, variations in candidate_data:
      # store best match for each candidate, keyed by quality of match (certainty)
      variation, certainty = closestvariation(txt, variations, method)
      if certainty not in results:
         results[certainty] = [(candidate, normalized, variation)]
      else:
         results[certainty].append((candidate, normalized, variation))

   bestquality = min(results) # get best result of them all (results ~ results.keys())
   _bestmatches = results[bestquality]  # (txt, cleaned, variation)
   mc = len(_bestmatches) # matchcount

   if bestquality <= maxdiff:

      if mc == 1: # single match, ok
         match = _bestmatches if multiple else _bestmatches[0]
         return (bestquality, match)

      else:
         if multiple: # multiple equally good matches allowed, ok
            return (bestquality, _bestmatches)
         if matchlen: # try to reduce ambiguity based on length matching
            lengths = [len(m[1]) for m in _bestmatches] # normalized lengths
            txtlen = len(txt)
            closest_length = min(lengths, key=lambda x:abs(x-txtlen))
            bestcount = lengths.count(closest_length)

            # If one of the matching alternatives is alone the closest to the length of the
            # term, and its lenght does not differ (too much) from the length
            # of the term, and the next closest differs clearly more, we choose it.
            if bestcount == 1:
               lengths.remove(closest_length)
               second_closest_length = min(lengths, key=lambda x:abs(x-txtlen))

               shortest_len_diff = abs(closest_length-txtlen)
               second_shortest_len_diff = abs(second_closest_length-txtlen)
               if shortest_len_diff <= 3 and (second_shortest_len_diff >= 2 * shortest_len_diff):
                  for m in _bestmatches:
                     if len(m[1]) == closest_length:
                        return (bestquality, m)

         # fall through to ambiguous failure
         errstr = "%i matches for %s found with confidence %f: %s"
         errdata = (mc, txt, bestquality, ", ".join((m[0] for m in _bestmatches)))
         raise AmbiguousMatchError(errstr % errdata, txt, bestquality, _bestmatches)

   # no match; do some more custom checking
   else:
      # if the length of term is at least 5 and half of the normalized low-quality match,
      # and it is verbatim part of the match, we accept the match as a special case
      specialcases = []
      for match in _bestmatches:
         nm = match[1]
         nmlength = len(nm)
         if txt in nm and nmlength >= 5 and nmlength >= (nmlength - nmlength/2):
            specialcases.append(match)
      if len(specialcases) == 1:
         return (bestquality, specialcases[0])

      # we give up; handle failure
      errstr = "no good match found, closest (%f) to %s is/are: %s"
      candidates = ', '.join((m[0] for m in _bestmatches))
      errdata = (bestquality, txt, candidates)
      raise NoMatchError(errstr % errdata, txt, bestquality, _bestmatches)
