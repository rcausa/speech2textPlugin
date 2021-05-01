import json
from num2words import num2words
import glob
"""
Create key : value pairs where the key is a transcribed word, and
the value is the Linux CLI command/option/file path which can be accessed.

This dictionary will be used to create commands from user voice input.

TO DO:
- make sure all keys unique
- reduce number of commands with >1 word
"""

commands = {
    # trying to limit to one-word cmds to limit the logic involved!
    "open" : "open",
    # "search" : "find", # wanted to make it more 'natural language'
    "find" : "find",
    "list" : "ls",
    "print" : "pwd",
    "change" : "cd",
    "remove" : "rm",
    "make" : "mkdir",
    # make is a command already
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
    "left square" : "[",
    "right square" : "]",
    "left curly" : "{",
    "right curly" : "}",
    "left parenthesis" : "(",
    "right parenthesis" : ")",
    "left angle" : "<",
    "right angle" : ">",
    "star" : "*",
    "hash" : "#",
    "bang" : "!",
    "dollar" : "$",
    "hat" : "^",
    "ampersand" : "&",
    "zero" : "0"
}

""" 
Convert spoken numbers (as transcribed by AssemblyAI)
into letters, including captial letters, to be used as options for commands
Need to remove dashes from num2words 'twenty-four' => 'twenty four'
"""

# Use the word 'one' to refer to the letter 'a'
# use the prefix 'capital' to find the capital version 'A'
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


""" 
Add list of Applications on the computer 
"""

apps = glob.glob("/Applications/*")
# remove all but the application name
apps = [app.split("/")[-1][:-4] for app in apps if '.app' in app] 
# unavoidably hand-done, and will skip several on purpose
app_keys = ['mendeley','visual','','signal','chrome','','','','','','','word','','acrobat','octave','safari','amphetamine','excel','blender','zoom','outlook','','','','','','fiji','','atom','charm','postman','powerpoint','teams','']
# Check they align correctly:
for i in range(len(apps)):
    print(f"{i:} {apps[i]:<26} {app_keys[i]}")

application_dict = dict(zip(app_keys, apps))
application_dict.pop("") # have one unique key which is an empty string, which should be removed.



""" Create final dictionary """
final = dict({})
final.update(commands)
final.update(symbols)
final.update(lowercase)
final.update(uppercase)
final.update(application_dict)

for k,v in final.items():
    print(f"{k :<25} {v}")

with open('keywords.json','w') as f :
    json.dump(final,f)