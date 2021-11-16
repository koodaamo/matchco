Match organization names. See docs/ directory for more info.

Basic usage:

    from matchco import normalized, subsequences, NoMatchError, bestmatch
    name = "mygreat korp"
    nname = normalized(name)
    candidates = (
       ("My Great Corp Inc.", "My Great Corp", ("my", "my great", "my great corp", "great corp", "corp")),
       ("Other Corp Inc.", "Other Corp", ("other", "corp", "other corp"))
    )
    try:
        match = bestmatch(nname, candidates, multiple=True)
    except NoMatchError:
        match = None
    print(match or "no match for '%s' found" % name)
