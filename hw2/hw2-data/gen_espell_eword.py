import collections
import numpy

print("EOS")

words_list = []
filepath = '/home/prachi/Desktop/CS 539_NLP/hw_2/hw2-data/hw2-data/eword-epron.data'

with open(filepath) as fp:
    line = fp.read().rstrip()
    lines = line.split("\n")

    for line in lines:
    	wrd = line.split(' ')[0]
    	words_list.append(wrd)

viewed = []
a_to_z = ['A','B','C','D','E','F','G','H','I','J','K','L',
			'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
for ch in a_to_z:
	print("(0 ({} {} *e*))".format(ch, ch))
	store = "(0 (" +ch+ " "+ch+"))"
	viewed.append(store)

for word in words_list:

	for i in range(len(word)):
		curr_state = word[:i+1]
		if (i+1) == len(word):
			store = "("+curr_state+ " (EOS *e*))"
			if store not in viewed:
				print("({} (EOS *e* {}))".format(curr_state, curr_state))
				viewed.append(store)
			break
		else:
			input_char = word[i+1]
		next_state = curr_state + input_char
		store = "("+curr_state+ " (" +next_state+ " "+input_char+"))"
		if store not in viewed:
			# then print
			print("({} ({} {} *e*))".format(curr_state, next_state, input_char))
			viewed.append(store)
		else:
			# otherwise don't print
			continue