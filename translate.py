import re
import sys
import pickle
import random
from transate_module import translate_to_pirate
# f = open('pirate_tongue.p','rb')
# pirate_tongue_dictionary = pickle.load(f)
# f.close()

# pirate_tongue_dictionary = {'Hello':'Ahoy'}


# Read phrases to be looked up and make a dictionary
f = open('pirate_translations.txt','r')
pirate_tongue_dictionary = {}
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    english_phrase,pirate_phrase = line_content.split(',')
    pirate_tongue_dictionary[english_phrase] = pirate_phrase

# Read exclamations and build a list of them
exclamations = []
f = open('pirate_exclamations.txt','r')
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    exclamations.append(line_content)


# Read users input, swap out phrases with pirate phrases
user_input = sys.argv[1]

print(translate_to_pirate(user_input))
