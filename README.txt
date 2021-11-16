Match organization names. See docs/ directory for more info.

Basic usage:

    from matchco import normalized, subsequences, NoMatchError, bestmatch
    name = "mygreat korp"
    nname = normalized(name)
    candidate1 = ("My Great Corp, Inc.", "My Great Corp", subsequences("My Great Corp".lower()))
    candidate2 = ("Other Corp Inc.", "Other Corp", subsequences("Other Corp Inc.".lower()))
    candidates = (candidate1, candidate2)
    try:
        match = bestmatch(nname, candidates, multiple=True)
    except NoMatchError:
        match = None
    print(match or "no match for '%s' found" % name)
