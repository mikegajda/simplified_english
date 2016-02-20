#A program that "translates" a word from traditional English to Simplified English
import urllib
import re
from xml.etree.ElementTree import parse

base_url = 'http://www.dictionaryapi.com/api/v1/references/'
key = '11907e1c-f7a5-496f-9c3a-048b307350af'
dictionary_type = 'collegiate'

translation_dict = {} #the dictionary containing the characters to be changed
translation_dict[u"\u0113"] = 'ee' # long e (ex. k\ee\p)
translation_dict[u"\u012B"] = 'ii' # long i (ex. k\i\te)
translation_dict[u"\u0101"] = 'aa' # long a (ex. c\a\pe)
translation_dict[u"\u014D"] = 'oo' # long o (ex. c\o\pe)
translation_dict[u"\u00FC"] = 'ou' # the oo (ex. f\oo\d)
translation_dict[u"\u0065"] = 'e'  #replaces the "short e" of various spellings (ex. l\e\t, s\ai\d, h\ea\d) with an "e"
translation_dict[u"\u0259"] = '-' #schwa
translation_dict[u"\u022F"] = 'au' # replaces c\augh\t with au

def build_url(word):
	return base_url + dictionary_type + "/xml/" + word + "?key=" + key #returns the url to look up the word

def pronunciation(word):
	entry = parse(urllib.urlopen(build_url(word))).getroot() #opens the url
	pr_list = []
	for elem in entry.iterfind('entry/pr'):
		pr_list.append(elem.text.encode('utf-8')) #traverses the xml and adds the pronunciation to the pr_list list
	pr = re.sub("-", '', pr_list[0]) #cleans up the pronunciation
	return pr.decode("utf-8").replace(u"\u02C8", "").encode("utf-8") #continues to clean up the pronunciation and encodes as UTF-8

def clean_up(word):
	"""Accepts a word and then returns it cleaned up by taking out some extraneous characters"""
	if len(word) == 1:
		return word
	else:
		if word[0] == ",":
			return ""
		elif word[0] == "(" or word[0] == ")":
			return "" + clean_up(word[1:])
		else:
			return word[0] + clean_up(word[1:])

def vowel_list(word):
	"""Checks which vowels are in the list"""
	my_list = []
	for character in word:
		if character in "aeiou-":
			my_list += [character]
	return my_list

def replace_dash(word, list):
	if len(list) == 0:
		return word
	else:
		if word[0] in "aeiou-":
			new_spelling = list[0] + replace_dash(word[1:], list[1:])
			return new_spelling
		else:
			new_spelling = word[0] + replace_dash(word[1:], list[:])
			return new_spelling

def find_duplicate_vowel(list):
	for index in range(len(list)-1):
		if (list[index] == list[index + 1]) and ((list[index] in "aeiou") and (list[index + 1] in "aeiou")):
			return True
	return False

def schwa(new_spelling, original_spelling):
	original_spelling_vowel_list = vowel_list(original_spelling)
	new_spelling_vowel_list = vowel_list(new_spelling)
	original_vowel_count = len(original_spelling_vowel_list)
	new_vowel_count = len(new_spelling_vowel_list)

	if (original_vowel_count == 1) and ("-" in new_spelling):
		new_spelling = new_spelling.replace("-", original_spelling_vowel_list[0])
	elif (new_vowel_count == original_vowel_count) and ("-" in new_spelling) and (find_duplicate_vowel(new_spelling_vowel_list) == False):
		# for index in range(len(original_spelling_vowel_list)):
			# if original_spelling_vowel_list[index] !=  new_spelling_vowel_list[index]:
				# new_spelling_vowel_list[index] = original_spelling_vowel_list[index]
		return replace_dash(new_spelling, original_spelling_vowel_list)
	return new_spelling



def translate(word):
	pr = pronunciation(word)
	pr_new = pr
	keys = translation_dict.keys() #this is a list of the characters to search for
	change_count = 0
	for entry in keys: #iterates over the traslation dictionary, translation_dict
		if entry in pr_new.decode("utf-8"): #if the character exists in the pronunciation of the word, it replaces it with the key from the dictionary
			change_count = change_count + 1
			pr_new = pr_new.replace(entry.encode("utf-8"), translation_dict[entry].encode("utf-8"))
	if change_count == 0:
		return word #if there was no match with any of the characters in the dictionary, return the word
	else:
		return schwa(clean_up(pr_new), word) #if there was a match, return the translated word

# def simplify_english(input):
	# return translate(input) #takes the inputted word and returns the translated version

# def simplify_english(input):
	# sentence_list = sentence_parse(input)
	# for word in sentence_list:
		# sentence_list[sentence_list.index(word)] = translate(word)
	# return sentence_list

print translate("president")

