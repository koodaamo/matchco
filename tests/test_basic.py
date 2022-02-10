# encoding: utf-8
import os
import pytest

from matchco import subsequences, closestvariation, bestmatch, normalized
from matchco import NoMatchError, AmbiguousMatchError
from util import generate_test_data, candidate_data


TESTDATA_FILE = "data/matches.csv"
testdata = list(generate_test_data(TESTDATA_FILE))
candidatedata = candidate_data(testdata)


# basic validation

def test_01_namevariations_return_strs():
   name = "Etelä-Suomen Rakennus- ja Purkutekniikka Oy"
   alts = subsequences(name)
   for a in alts:
      assert type(a) == str


# test variation generation

def test_02_namevariations_with_umlaut_end():
   name = "Ryhmä Rämä Oy"
   alts = subsequences(name, normalize=normalized)
   assert set(alts) == set(("rämä", "ryhmä rämä", "ryhmä"))


# test different methods

def test_031_basic_jaccard():
   name = "Etelä-Suomen Rakennus- ja Purkutekniikka Oy"
   tested = "Rakennus- japurkuteknikka"
   alts = subsequences(name, normalize=normalized)
   assert closestvariation(tested, alts, "jaccard")[1] < 0.22

def test_032_basic_levenshtein():
   name = "Etelä-Suomen Sähläys- ja Purkutekniikka Oy"
   tested = "Sähläys- japurkuteknikka"
   alts = subsequences(name, normalize=normalized)
   assert closestvariation(tested, alts, "levenshtein")[1] < 0.46

def test_033_basic_damerau():
   name = "Etelä-Suomen Sähläys- ja Purkutekniikka Oy"
   tested = "Sähläys- japurkuteknikka"
   alts = subsequences(name, normalize=normalized)
   assert 0 < closestvariation(tested, alts, "damerau")[1] < 0.4

def test_034_basic_sorensen():
   name = "Etelä-Suomen Rakennus- ja Purkutekniikka Oy"
   tested = "Rakennus- japurkuteknikka"
   alts = subsequences(name, normalize=normalized)
   assert closestvariation(tested, alts, "sorensen")[1] < 0.22


# test cases when there are multiple matches

def test_041_multiple_matches():
   "multiple equally good matches are produced"

   name = "Sarat"
   alts = [
     ("SARATI OY", "sarati", [u'sarati']),
     ("SARATO OY", "sarato", [u'sarato']),
     ("TOINEN", "toinen", [ u'toinen'])
   ]

   result = [('SARATI OY', u'sarati', u'sarati'), ('SARATO OY', u'sarato', u'sarato')]
   assert bestmatch(name, alts, multiple=True)[1] == result


def test_042_multiple_nomatches():
   name = "IhanJokuMu"
   alts = [
     ("SARATTI OY", "saratti", [u'saratti', u'sarat']),
     ("Oy SARAT", "sarat", [u'sarat']),
     ("TOINEN", "toinen", [u'toinen'])
   ]
   with pytest.raises(NoMatchError) as e_info:
      assert bestmatch(name, alts, multiple=True)

def test_051_select_match_closestsize_found():
   name = u'YIT'
   alts = [
     ("YIT OY", "yit", [u'yit']),
     ("YITT OY", "yitt", [u'yit']),
     ("YIT Rakennus Oy", "yit rakennus", [u'yit', u'rakennus']),
     ("YIT VESI", "yit vesi", ["yit", u'vesi']),
     ("YII OY", "yii", [u'yii']),
   ]
   assert bestmatch(name, alts, multiple=False)[1] == (u'YIT OY', u'yit', u'yit')


def test_052_select_match_closestsize_ambiguous():
   name = u'YITP'
   alts = [
     ("YIT OY", "yit", [u'yit']),
     ("YITO OY", "yito", [u'yito']),
     ("YITL OY", "yitl", [u'yitl']),
     ("YIT Rakennus Oy", "yit rakennus", [u'yit', u'rakennus']),
     ("YIT VESI", "yit vesi", ["yit", u'vesi']),
     ("YII OY", "yii", [u'yii']),
   ]
   with pytest.raises(AmbiguousMatchError):
      bestmatch(name, alts, multiple=False)


@pytest.mark.parametrize("expected, inputs", testdata)
def test_06_match(expected, inputs):
   for name in inputs:
      assert bestmatch(name, candidatedata, method="damerau")[1][0] == expected
