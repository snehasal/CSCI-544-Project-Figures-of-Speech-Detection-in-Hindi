#coding:UTF-8
import re
import sys
labelData = 'sent_sim.txt'
trainData = 'correct sentences.txt'

#defining lists
stopword_list = ['के', 'का', 'एक', 'में', 'है', 'यह', 'और', 'से', 'हैं', 'को', 'पर', 'इस', 'होता', 'कि', 'जो', 'कर', 'मे', 'गया', 'करने', 'किया', 'लिये', 'अपने', 'ने', 'बनी', 'नहीं', 'तो', 'ही', 'या', 'एवं', 'दिया', 'हो', 'इसका', 'था', 'द्वारा', 'हुआ', 'तक', 'साथ', 'करना', 'वाले', 'बाद', 'लिए', 'आप', 'कुछ', 'सकते', 'किसी', 'ये', 'इसके', 'सबसे', 'इसमें', 'थे', 'दो', 'होने', 'वह', 'वे', 'करते', 'बहुत', 'कहा', 'वर्ग', 'कई', 'करें', 'होती', 'अपनी', 'उनके', 'थी', 'यदि', 'हुई', 'जा', 'ना', 'इसे', 'कहते', 'जब', 'होते', 'कोई', 'हुए', 'व', 'न', 'अभी', 'जैसे', 'सभी', 'करता', 'उनकी', 'उस', 'आदि', 'कुल', 'एस', 'रहा', 'इसकी', 'सकता', 'रहे', 'उनका', 'इसी', 'रखें', 'अपना', 'पे', 'उसके']
punctuation_list = {';', '~', '+', "'", ',', '.', '%', '_', '[', '{', '`', '<', '\\', '=', '*', '!', '/', '}', '"', ':', '@', ')', ']', '$', '?', '(', '#', '-', '|', '&', '>', '^','‘', '’', '”', '“',''}
training_token_list = []
ff = open('nbmodel.txt', 'w', encoding="utf-8-sig")

#separate review with next line character

paragraph_review_list = [list.rstrip('\n') for list in open(trainData, encoding="utf-8-sig")]

#convert all elements to lowercase, remove stopwords, remove punctuations, filter null values
for j in range(len(paragraph_review_list)):
    intermediate = []
    intermediate = paragraph_review_list[j].split(' ')
    intermediate = [element.lower() for element in intermediate]
    for k in range(len(intermediate)):
        intermediate[k] = ''.join(ch for ch in intermediate[k] if ch not in punctuation_list)
    xyz = set(intermediate) - set(stopword_list)
    intermediate = list(xyz)
    intermediate = list(filter(None, intermediate))
    training_token_list.append(intermediate)

print(training_token_list)

#create label lists for two binary classifiers
list_of_labels = [list.rstrip('\n') for list in open(labelData,'r')]


list_of_tokens = []
for list in training_token_list:
    for i in list:
        if i not in list_of_tokens:
            list_of_tokens.append(i)


#function to calculate occurances of a particular token in a particular class
#returning counter + 1 for add-one smoothing
# g=0
pos1=0
neg1=0

for c in list_of_labels:
    if(c=="SIMILE"):
        pos1+=1
    else:
        neg1+=1

prior={}
prior['p']=pos1/float(pos1+neg1)
prior['n']=neg1/float(pos1+neg1)
# prior['t']=tru1/float(pos1+neg1)
# prior['d']=dec1/float(pos1+neg1)
i=-1
dict1 = dict()
for r in training_token_list:
    i=i+1
    for w in r:
        if w in dict1:
            if (list_of_labels[i]=="SIMILE"):
                dict1[w][2]= dict1[w][2]+1
            else:
                dict1[w][3]=dict1[w][3]+1

        else:
            dict1[w]=[1,1,1,1]

            if (list_of_labels[i]=="SIMILE"):
                dict1[w][2]= dict1[w][2]+1
            else:
                dict1[w][3]=dict1[w][3]+1


pos=0
neg=0

for key,value in dict1.items():
    pos += value[2]
    neg += value[3]

for key,val in dict1.items():
    dict1[key][2]/=float(pos)
    dict1[key][3]/=float(neg)

for i in dict1:
    ff.write(i)
    ff.write(' ')
    ff.write(str(dict1[i][2]))
    ff.write(' ')
    ff.write(str(dict1[i][3]))
    ff.write('\n')
ff.write('$')
ff.write('\n')
