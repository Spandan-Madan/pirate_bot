import re
import sys
import pickle
import random
# f = open('pirate_tongue.p','rb')
# pirate_tongue_dictionary = pickle.load(f)
# f.close()

# pirate_tongue_dictionary = {'Hello':'Ahoy'}


# Read phrases to be looked up and make a dictionary
f = open('phrase_translations.txt','r')
pirate_phrase_dictionary = {}
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    english_phrase,pirate_phrase = line_content.split(',')
    pirate_phrase_dictionary[' ' + english_phrase ] = ' ' + pirate_phrase

# Read words to be looked up and make a dictionary
f = open('word_translations.txt','r')
pirate_words_dictionary = {}
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    english_word,pirate_words = line_content.split(',')
    pirate_words_dictionary[english_word ] = pirate_words



# Read exclamations and build a list of them
exclamations = []
f = open('pirate_exclamations.txt','r')
content = f.readlines()
f.close()

for line_content in content:
    line_content = line_content.rstrip()
    exclamations.append(line_content)

def replace_phrases(input):
    for key in pirate_tongue_dictionary.keys():
        output = re.sub(key,pirate_tongue_dictionary[key],input.lower())
    return output

def replace_words(input):
    words = re.split('(\W+)', input)
    pirate_words = []
    for word in words:
        if word in pirate_words_dictionary.keys():
            pirate_words.append(pirate_words_dictionary[word])
        else:
            pirate_words.append(word)

    for j in range(len(words)):
        word = words[j]
        if 'ing' in word:
            if random.uniform(0,1) < 0.7:
                words[j] = re.sub("ing","in'",word)
    return words

def add_exclamations(words):
    if words[0] == 'ahoy':
        sentence = ''.join(words)
    else:
        random_start = random.choice(exclamations)
        sentence = random_start + ''.join(words)

    sentence.replace("\\","")
    return sentence

def translate_to_pirate(input):
    replaced_phrases = replace_phrases(input)
    replaced_words = replace_words(replaced_phrases)
    final_sentence = add_exclamations(replaced_words)

    return final_sentence


########### Ignore below. Legacy code retained in case we need to restructure when adding new functionality ###############
# Read input, swap out phrases with pirate phrases
# def translate_to_pirate(input):
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


    # Add random exclamation in beginning if it doesn't start with hello!

    # for j in range(len(words)):
    #     word = words[j]
    #     if 'ing' in word:
    #         if random.uniform(0,1) < 0.7:
    #             words[j] = re.sub("ing","in'",word)
    #
    # if words[0] == 'ahoy':
    #     sentence = ''.join(words)
    # else:
    #     random_start = random.choice(exclamations)
    #     sentence = random_start + ''.join(words)
    #
    #
    # return sentence
