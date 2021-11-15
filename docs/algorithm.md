# Goal
The purpose of the algorithm is to help automatically determine (with an acceptable certainty) what organization (legal business entity) name an input string refers to.

# Input
The algorithm is first provided a list of valid legal organization names that the input string is matched to.

After that, it is given an organization name (the input string) that has been manually entered by a person, possibly using a small keypad or touchscreen.

# Challenges
1. The organization name entered as input string may contain typos, misunderstandings and other errors.
2. It may or may not contain a reference to the type of organization (legal entity name abbreviation, such as ”ltd” or ”oy”), and the type may be prefixed, suffixed or it may appear in the middle. Furthermore, some names may have multiple such legal type terms, as in ”Oy Firma Ab Ltd”. All of which might appear in input string - or not.
3. In many business domains, there are terms that are commonly used as part of the business name. For example in logistics, the words ”transport” and ”logistics” often appear in names, and likewise ”building” or ”construction”, in construction industry business names. These kind of common terms are often omitted by people entering the organization name using for example a mobile phone, or when speaking of the organization with other people familiar with the (same) domain that are thus still bound to know what organization the shortened name refers to.

# Implementation

To match the input to a valid organization name, above mentioned challenges must be considered.

Given the above mentioned issues #2 and #3, we can improve the chance of correct match by:

1. removing legal entity names from organization names
2. matching against partial sequences of the organization names

Finally, to overcome small differences such as typos, string differences algorithms are used. In particular, Jaccard distance algorithm has been said to be better for difference measurement of company names than Levenshtein distance.