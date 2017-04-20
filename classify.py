import re
import math
import sys

testdata = 'test_correct_sentences.txt'
stopword_list = ['के', 'का','एक', 'में', 'है', 'यह', 'और', 'से', 'हैं', 'को', 'पर', 'इस', 'होता', 'कि', 'जो', 'कर', 'मे', 'गया', 'करने', 'किया', 'लिये', 'अपने', 'ने', 'बनी', 'नहीं', 'तो', 'ही', 'या', 'एवं', 'दिया', 'हो', 'इसका', 'था', 'द्वारा', 'हुआ', 'तक', 'साथ', 'करना', 'वाले', 'बाद', 'लिए', 'आप', 'कुछ', 'सकते', 'किसी', 'ये', 'इसके', 'सबसे', 'इसमें', 'थे', 'दो', 'होने', 'वह', 'वे', 'करते', 'बहुत', 'कहा', 'वर्ग', 'कई', 'करें', 'होती', 'अपनी', 'उनके', 'थी', 'यदि', 'हुई', 'जा', 'ना', 'इसे', 'कहते', 'जब', 'होते', 'कोई', 'हुए', 'व', 'न', 'अभी', 'जैसे', 'सभी', 'करता', 'उनकी', 'उस', 'आदि', 'कुल', 'एस', 'रहा', 'इसकी', 'सकता', 'रहे', 'उनका', 'इसी', 'रखें', 'अपना', 'पे', 'उसके']
final_list = []
character_seq = []
truthful = []
deceptive = []
positive = []
negative = []
list_sep = []
file_contents = []
index_list = []

out_file = open('nboutput.txt', 'w',encoding="utf-8")
in_file = open('nbmodel.txt',encoding="utf-8")
content = in_file.read()
list_sep = content.split('\n')
print(list_sep)

for str in list_sep:
    tl = str.split(' ')
    if tl.__contains__(''):
      tl.remove('')
    file_contents.append(tl)

file_contents.remove(file_contents[len(file_contents)-1])
print(file_contents)


for i in range(len(file_contents)):
    if file_contents[i][0] == '$':
        index_list.append(i)

priors = []
dict1 = dict()
for i in range(index_list[0]):
    dict1[file_contents[i][0]] = [file_contents[i][1], file_contents[i][2]]

print(dict1)

for i in range(index_list[0] + 1, len(file_contents)):
    priors.append(file_contents[i])

print(priors)

list_fin = [list.rstrip('\n') for list in open(testdata,encoding="utf-8")]

for j in range(len(list_fin)):
    temp_list = []
    temp_list = list_fin[j].split(' ')
    temp_list = set(temp_list) - set(stopword_list)
    temp_list = list(temp_list)
    temp_list = [element.lower() for element in temp_list]
    temp_list = list(filter(None, temp_list))
    final_list.append(temp_list)

print(final_list)


def calculate_probability(token, classification1):
    if (token not in dict1):
        return 1.0
    elif classification1 == 'SIMILE':
        return dict1[token][0]
    elif classification1 == 'NOT':
        return dict1[token][1]
#
#
l = len(final_list)
w = 2
review_classification = [[0 for x in range(w)] for y in range(l)]
m = 0
n = 0
# o = 0
# p = 0
somevar = 0
for i in final_list:
    for j in i:
        m += math.log(float(calculate_probability(j, 'SIMILE')), 10)
        n += math.log(float(calculate_probability(j, 'NOT')), 10)
    review_classification[somevar][0] = m
    review_classification[somevar][1] = n
    m = 0
    n = 0
    somevar += 1

# writing output to a text file
for i in range(len(review_classification)):
    # out_file.write(character_seq[i])
    # out_file.write(' ')
    if review_classification[i][0] > review_classification[i][1]:
        out_file.write('SIMILE'.strip())
    else:
        out_file.write('NOT'.strip())

    out_file.write('\n')