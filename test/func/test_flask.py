from main.run import *


def test_counter():
    text = "this is test"
    words_count, words = counter(text)
    assert len(words_count)>0

