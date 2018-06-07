import re
import sys
import pickle
import random
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
    pirate_tongue_dictionary[' ' + english_phrase ] = ' ' + pirate_phrase

# Read exclamations and build a list of them
exclamations = []
f = open('pirate_exclamations.txt','r')
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    exclamations.append(line_content)


# Read input, swap out phrases with pirate phrases
def translate_to_pirate(input):
    #
    # pirate_words = []
    #
    # for i in range(len(words)):
    #     word = words[i]
    #     bigram_phrase = ''.join(word[i:i+3])
    #     trigram_phrase = ''.join(word[i:i+5])
    #
    #     if word in pirate_tongue_dictionary.keys():
    #         pirate_words.append(pirate_tongue_dictionary[word])
    #     elif bigram_phrase in pirate_tongue_dictionary.keys():
    #         pirate_words.append(pirate_tongue_dictionary[bigram_phrase])
    #         i += 1
    #     elif trigram_phrase in pirate_tongue_dictionary.keys():
    #         pirate_words.append(pirate_tongue_dictionary[trigram_phrase])
    #         i += 2
    #     else:
    #         pirate_words.append(word)

    for key in pirate_tongue_dictionary.keys():
        input = re.sub(key,pirate_tongue_dictionary[key],input.lower())
    # Add random exclamation in beginning if it doesn't start with hello!
    words = re.split('(\W+)', input)

    for j in range(len(words)):
        word = words[j]
        if 'ing' in word:
            if random.uniform(0,1) < 0.7:
                words[j] = re.sub("ing","in'",word)

    if words[0] == 'ahoy':
        sentence = ''.join(words)
    else:
        random_start = random.choice(exclamations)
        sentence = random_start + ''.join(words)

    sentence.replace("\\","")
    return sentence
