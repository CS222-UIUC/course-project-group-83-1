import data_clean


def test_regex():
    assert data_clean.regex("i'm don't can't") == "im dont cant"
    assert data_clean.regex("@abc #123") == " 123"
    assert data_clean.regex("https://regexr.com") == ""
    assert data_clean.regex("www.google.com") == ""
    assert data_clean.regex("`~!@#$%^&*()-=_+[]\\;',./|:\"<>?") == " "


def test_cleanTweets():
    # test stem
    text = """he likes playing baseball and basketball but is not fond of
            running or tennis"""
    assert "running" not in data_clean.cleanTweets(text)
    assert "play" in data_clean.cleanTweets(text)
    # test stop
    assert "he" not in data_clean.cleanTweets(text)
    assert "and" not in data_clean.cleanTweets(text)
    assert "is" not in data_clean.cleanTweets(text)
    assert "of" not in data_clean.cleanTweets(text)
    assert "or" not in data_clean.cleanTweets(text)
    assert "run" in data_clean.cleanTweets(text)
