import re
import string
from typing import Dict, List, Optional
from lemminflect import getAllInflections, getAllLemmas
import nltk.corpus
from nltk.corpus import words
import ssl


# ---------- Main Functions -------------

def find_words(word_list: List[str] = None,
                 num_letters: int|List[int] = None,
                 shorter_than: int = None,
                 longer_than: int = None,
                 includes_at_idxs: Dict[int,List[str]] = None,
                 excludes_at_idxs: Dict[int,List[str]] = None,
                 includes: List[str] = None, 
                 excludes: List[str] = None,
                 plural = None,
                 tense: str = None,
                 kinds: List[str] = None,
                 penn_tag: List[str] = None,
                 upos_tag: List[str] = None
                 ) -> List[str]:
  '''
  TODO - doctstring
  
  TODO - valid upos tags
  
  TODO - simple tense kwarg

  tense is just a plain english interface for penn tags
  {base : "VB", "past": ["VBP",], present: "VBD",}
  
  TODO - add plural and tense easy interface for
  common penn tag combos

  '''
  if word_list is None:
    word_list = get_full_word_list()

  poss_words = []
  
  # -----------  Redo This ------------
  
  if penn_tag is not None:
    
    for word in word_list:
      inflect_dict = getAllInflections(word, upos = upos_tag)
      for p_tag, inflections in inflect_dict.items():
        if p_tag == penn_tag:
              poss_words.extend(inflections)
  
  else:
    
    for word in word_list:
      inflect_dict = getAllInflections(word, upos = upos_tag)
      inflections = {item for tuple in inflect_dict.values() for item in tuple}
      poss_words.extend(inflections)

  # ------------------------------------------
  
  poss_words = {standardize_word(word) for word in poss_words}

  if num_letters is not None:
    poss_words = {w for w in poss_words if has_num_letters(w, num_letters)}
  elif shorter_than is not None:
    poss_words = {w for w in poss_words if has_num_letters(w, num_letters) < shorter_than}
  elif longer_than is not None:
    poss_words = {w for w in poss_words if has_num_letters(w, num_letters) > longer_than}

  if includes is not None:
    poss_words = {w for w in poss_words if includes_all(w, includes)}

  if excludes is not None:
    poss_words = {w for w in poss_words if excludes_all(w, excludes)}

  if includes_at_idxs is not None:
    poss_words = {w for w in poss_words if includes_letters_at_idxs(w, includes_at_idxs)}

  if excludes_at_idxs is not None:
    poss_words = {w for w in poss_words if excludes_letters_at_idxs(w, excludes_at_idxs)}
    
  return sorted(list(poss_words))


def get_full_word_list() -> List[str]:
  '''
  Returns the full nltk list of 236736 words. If not available tries to download
  the list and then return it.
  '''
  try:
    word_list = words.words()
  except LookupError:
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('words')
    word_list = words.words()
  return word_list



# ---------- Letter Filters ------------

def has_num_letters(word: str, num_letters: List[int]|int) -> bool:
  '''
    TODO - docstring
    '''
  word_len = len(get_char_list(word))

  match num_letters:
    case int():
      return word_len == num_letters
    case list():
      return word_len in num_letters


def standardize_word(word: str) -> str:
  '''
  Removes underscores, hyphens and apostrophes from a string.
  '''
  chars_to_remove = "_'-"
  pattern = f'[{chars_to_remove}]'

  return re.sub(pattern, "", word)


def get_char_list(word: str, preserve_case : bool = False) -> List[str]:
  '''
  Returns a list of characters that make up the input string. Letters are converted to lowercase unless 'preserve_case' is set to True.

  Args:
    word (str): String to get characters for
    preserve_case (bool, optional): Flag to set case behaviour. If True, will
        not change case of characters in 'word'.

  Returns:
    List[str]: A list of characters that make up the original string. 
  '''
  if preserve_case == True:
    return [char for char in word]
  else:
    return [char.lower() for char in word]


def alphabet() -> List[str]:
  '''
  Returns a list of all alphabet letters as lowercase strings.
  '''
  return [char for char in string.ascii_lowercase]


def includes_all(word: str, letter_list: List[str]) -> bool:
  '''
  Returns True if all letters in letter_list are present in the word string.

  Args:
    word (str): string to check whether it includes letters
    letter_list (list): List of lowercase alphabet letters to check are included
  '''

  return all([let in set(get_char_list(word)) for let in letter_list])


def excludes_all(word: str, letter_list: List[str]) -> bool:
  '''
  Returns True if none of the letters in letter_list are present in the word string.

  Args:
    word (str): string to check whether it includes letters
    letter_list (list): List of lowercase alphabet letters to check are not present.
  '''

  return all([let not in set(get_char_list(word)) for let in letter_list])


def includes_letters_at_idxs(word: str, idx_letter_dict: Dict[int, List[str]]) -> bool:
  '''
  Allows filtering of words by whether they include letters in certain places.

  Checks whether the provided word strings letters is one of
  the provided letters at every index. If 'idx_letter_dict' contains any indexes
  which are out of range of the word then this function returns False.

  Args:
    word (str): string to check
    idx_letter_list (dict): A dictionary whose keys are indexes and whose values are lists of lowercase letters.

  Returns:
    Bool: True if for every index/key provided in 'idx_letter_dict', the letter at
          that index in 'word' is included in the value/list of lowercase letters
          of idx_letter_dict
  
  Example::

      includes_letters_at_idxs("cat", {0:["a","b"], 2:["s","t"]}) -> True
      includes_letters_at_idxs("cat", {0:["a","b"], 2:["s"]}) -> False
  '''
  char_list = get_char_list(word)
  bool_list = []

  for idx, letter_list in idx_letter_dict.items():

    if idx >= len(char_list):
      return False
    else:
      curr_bool = any([char_list[idx] == c for c in letter_list])

    bool_list.append(curr_bool)

  return all(bool_list)


def excludes_letters_at_idxs(word: str, idx_letter_dict: Dict[int, List[str]]) -> bool:
  '''
    Allows filtering of words by whether they include letters in certain places.
  '''

  char_list = get_char_list(word)
  bool_list = []

  for idx, letter_list in idx_letter_dict.items():

    if idx >= len(char_list):
      curr_bool = True
    else:
      curr_bool = all([char_list[idx] != letter for letter in letter_list])

    bool_list.append(curr_bool)

  return all(bool_list)



# ---------- Parts of Speech ------------

def includes_penn_tag(word:str, penn_tags: List[str]) -> bool:
  '''
    TODO - docstring
    '''
  word_penn_tags = get_inflection_types(word)
  return any([w_tag in penn_tags for w_tag in word_penn_tags])

def get_inflection_types(word:str) -> bool:
  '''
    TODO - docstring
    '''

  base_words = get_all_base_words(word)
  inflect_types = []

  for base_word in base_words:
    inflect_dict = getAllInflections(base_word)
    for inf_type, inflect_words in inflect_dict.items():
      if word in inflect_words:
        inflect_types.append(inf_type)
  return inflect_types

def get_all_base_words(word: str) -> List[str]:
  '''
    TODO - docstring
    '''
  return list(set([tup[0] for tup in list(getAllLemmas(word).values())]))



