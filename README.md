# word-constraints

A small python module for finding words with included or excluded letters and letter positions, and by word type.

Originally made for use in word based puzzles such as wordle or crosswords.

# Example Uses

## Wordle Filtering
This demonstrates filtering by letter inclusion and exclusion, both over a whole word and at paticular positions.

Here we have a wordle game (spoilers for 30/08/2022):

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1FvXHPWbosbxWX0r3iEDrpRWY_ngr5ABR" height = "200">
</p>

At this point we know quite a lot of information about the target word:
- H,A,R,P,I,L,F,U and D are excluded from the word.
- An E is included at the 4th position.
- S,E,O and N are included somewhere in the word but those letters are not present at that position.

Using find_words we can find words that meet all these constraints:

![alt text](https://drive.google.com/uc?export=view&id=1v14b6GyHmK-4TvIS6YhKsNcdyGugvXtE)

And we find that there is only one word (in the default word list) that meets these constraints:


<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1KO7Ioy76Av1L3K2rW2w2HvO3ZTfv7_Ab" width="20%">
</p>

And sure enough that's the answer!

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1gVBIcrvnkCbdqeZdcEr26JPw3PaFX0xV" height = "200">
</p>



## Crossword Clues
This demonstrates the use of the "parts of speech" and penn tags functionality.

# Full Functionality

Basically all functionality is accessed using the find_words function.

find_words takes a few different parameters

# About

The default list of words for filtering is the nltk list of around 23,000 words.

Processing of word types leans heavily on [LemmInflect](https://github.com/bjascob/LemmInflect).

# Todos

- Add the ability to match the type of a provided word (useful for crosswords, where for example, a plural noun clue means the answer is also a plural noun)
- Change list filters to set comprehensions. 
- Remove isinstance type checking and use duck typing
- Make a more user friendly way to interact with universal parts of speech tags and penn tags

