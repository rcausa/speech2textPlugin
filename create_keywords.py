import json
from num2words import num2words
"""
Create key : value pairs where the key is a transcribed word, and
the value is the Linux CLI command/option/file path which can be accessed.

This dictionary will be used to create commands from user voice input.
"""

commands = {
    "open" : "open",
    "search" : "find",
    "find" : "find",
    "list" : "ls",
    "print working directory" : "pwd",
    "change directory" : "cd",
    "remove directory" : "rm",
    "make directory" : "mkdir",
    "move" : "mv",
    "copy" : "cp"
}


symbols = {
    "dot" : ".",
    "dash" : "-",
    "underscore" : "_",
    "slash" : "/",
    # "backslash" : "\\",
    "pipe" : "|",
    "left square bracket" : "[",
    "right square bracket" : "]",
    "left curly bracket" : "{",
    "right curly bracket" : "}",
    "left parenthesis" : "(",
    "right parenthesis" : ")",
    "left angle bracket" : "<",
    "right angle bracket" : ">",
}

# Two convert spoken numbers (as transcribed by AssemblyAI)
# into letters, including captial letters, to be used as options for commands
# Need to remove dashes from num2words 'twenty-four' => 'twenty four'

nums = list(range(ord('a'), ord('z')+1)) 
capital_nums = list(range(ord('A'), ord('Z')+1))

letter_symbols = list(map(chr, nums))
capital_letter_symbols = list(map(chr, capital_nums))

words = [None]*26
capital_prefix_words = [None]*26
for i in range(26):
    words[i] = " ".join(num2words(i+1).split('-'))
    capital_prefix_words[i] = 'capital ' + " ".join(num2words(i+1).split("-"))

# all lower and uppercase options possible
lowercase = dict(zip(words, letter_symbols))
uppercase = dict(zip(capital_prefix_words, capital_letter_symbols))

# Long lookup dictionary
final = dict({})
final.update(commands)
final.update(symbols)
final.update(lowercase)
final.update(uppercase)

for k,v in final.items():
    print(f"{k:25} {v}")

with open('keywords.json','w') as f :
    json.dump(final,f)