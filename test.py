import pytest
from wordconstraints.wordconstraints import *

# --------- get_char_list -----------


@pytest.mark.parametrize(
    "word, expected",
    [
        ("cat", ["c", "a", "t"]),
        ("Cat", ["c", "a", "t"]),
    ],
)
def test_get_char_list(word, expected):
    assert get_char_list(word) == expected


# --------- includes_at_idxs -----------


@pytest.mark.parametrize(
    "word, idx_letter_dict, expected",
    [
        ("octopus", {0: ["o"]}, True),  # one included
        ("octopus", {0: ["z"]}, False),  # one not included globally
        ("octopus", {0: ["o"], 1: ["c"]}, True),  # two included
        ("octopus", {0: ["c"]}, False),  # not included at idx but is globally
        ("octopus", {0: ["o", "z"], 1: ["c"]}, True),  # two included with extras
        ("octopus", {0: ["o", "z"], 1: ["z"]}, False),  # one idx passes and one doesn't
        ("octopus", {15: ["z"]}, False),  # out of range counts as excluded
        ("Paris", {0: ["r"]}, False),  # case insensitive exclusion
        ("Paris", {0: ["p"]}, True),  # case insensitive inclusion
    ],
)
def test_includes_at_idxs(word, idx_letter_dict, expected):
    assert includes_letters_at_idxs(word, idx_letter_dict) is expected


# --------- excludes_at_idxs -----------


@pytest.mark.parametrize(
    "word, idx_letter_dict, expected",
    [
        ("octopus", {0: ["o"]}, False),  # one included
        ("octopus", {0: ["z"]}, True),  # one globally excluded
        ("octopus", {0: ["c"]}, True),  # one globally included, one idx
        ("octopus", {0: ["o"], 1: ["c"]}, False),  # two included
        ("octopus", {0: ["y"], 1: ["z"]}, True),  # both globally excluded
        ("octopus", {0: ["o"], 1: ["z"]}, False),  # one included globally, multi idx
        ("octopus", {0: ["c"], 1: ["z"]}, True),  # one globally included, multi idx
        ("octopus", {0: ["o", "z"]}, False),  # one included and one not at idx
        ("octopus", {0: ["o", "z"], 1: ["z"]}, False),  # one idx excluded and one not
        ("octopus", {0: ["c", "z"]}, True),  # one globally included at same idx
        ("octopus", {0: ["c", "s"], 1: ["o"]}, True),  # all globally included
        ("octopus", {15: ["z"]}, True),  # out of range counts as excluded
        ("Paris", {0: ["r"]}, True),  # case insensitive exclusion
        ("Paris", {0: ["p"]}, False),  # case insensitive inclusion
    ],
)
def test_excludes_at_idxs(word, idx_letter_dict, expected):
    assert excludes_letters_at_idxs(word, idx_letter_dict) is expected


# --------- includes_all -----------


@pytest.mark.parametrize(
    "word, num, expected",
    [
        ("cat", ["c"], True),
        ("cat", ["b"], False),
        ("cat", ["b", "c"], False),
        ("Cat", ["c"], True),
    ],
)
def test_includes_all(word, num, expected):
    assert includes_all(word, num) is expected


# --------- excludes_all -----------


@pytest.mark.parametrize(
    "word, num, expected",
    [
        ("cat", ["z"], True),
        ("cat", ["a"], False),
        ("cat", ["b", "c"], False),
        ("Cat", ["c"], False),
    ],
)
def test_excludes_all_one(word, num, expected):
    assert excludes_all(word, num) is expected


# --------- is_shorter_than -----------


@pytest.mark.parametrize(
    "word, num, expected", [("cat", 4, True), ("cat", 3, False), ("cat", 2, False)]
)
def test_is_shorter_than(word, num, expected):
    assert is_shorter_than(word, num) is expected


# --------- is_longer_than -----------


@pytest.mark.parametrize(
    "word, num, expected", [("cat", 4, False), ("cat", 3, False), ("cat", 2, True)]
)
def test_is_longer_than(word, num, expected):
    assert is_longer_than(word, num) is expected


# --------- has_num_letters -----------


@pytest.mark.parametrize(
    "word, num, expected", [("cat", 4, False), ("cat", 3, True), ("cat", 2, False)]
)
def test_has_num_letters(word, num, expected):
    assert has_num_letters(word, num) is expected


# --------- standardize_word -----------


@pytest.mark.parametrize(
    "word, expected",
    [("cat-o'-nine-tails", "catoninetails"), ("hi_hello'-", "hihello")],
)
def test_standardize_word(word, expected):
    assert standardize_word(word) == expected


# --------- find_words -----------
# TODO add tests for excludes at index

def test_find_words():
    # only 5 letter word with "lbu" in the middle is "album"
    assert find_words(
        num_letters=5, includes_at_idxs={1: ["l"], 2: ["b"], 3: ["u"]}
    ) == ["album"]
    # only 6 letter word ending in "mt"
    assert find_words(num_letters=6, includes_at_idxs={4: ["m"], 5: ["t"]}) == [
        "dreamt"
    ]
    # only 7 letter word without a,e,i,o,u
    assert find_words(num_letters=7, excludes=["a", "e", "i", "o", "u"]) == ["rhythms"]
    # only 6 letter word that can be made out of letters c,a,v,i,t,y
    assert find_words(num_letters=6, includes=["c", "a", "v", "i", "t", "y"]) == [
        "cavity"
    ]

# TODO upos tag tests

# TODO penn tag tests

# TODO apply multiple filters tests
