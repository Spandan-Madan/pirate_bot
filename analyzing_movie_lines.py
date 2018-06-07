import enchant

english_words = enchant.Dict("en_US")

f = open('movie_lines.txt','r')
content = f.readlines()
f.close()

pirate_words_uncleaned = []
for c in content:
    c = c.rstrip()
    words = c.split()
    for word in words:
        if english_words.check(word) == False:
            pirate_words_uncleaned.append(word)
    pirate_words_uncleaned = list(set(pirate_words_uncleaned))

print(pirate_words_uncleaned)
