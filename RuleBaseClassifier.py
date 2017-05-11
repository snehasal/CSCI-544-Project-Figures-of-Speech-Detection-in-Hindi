test_sentence_file = open('test_correct_sentences.txt', 'r', encoding="utf-8-sig")
output_label_file = open('nboutput.txt','r',encoding="utf-8-sig")
output_final_file = open('final_ouput','w',encoding="utf-8-sig")
test_sentences = [list.rstrip('\n') for list in test_sentence_file]

sentence_word_list = []
for sentence in test_sentences:
    word_list = sentence.split(' ')
    sentence_word_list.append(word_list)

# print(sentence_word_list)

label_list = [list.rstrip('\n') for list in output_label_file]

# print(label_list)

#sneha code starts
ff= open('hindi.output', 'r', encoding="utf-8")
content = ff.readlines()

listword=list()
listtag=list()
listnum=list()
tempword=[]
temptag=[]
tempnum=[]

for line in content:
    word = line.split()
    if len(word)==0:
        listtag.append(temptag)
        listword.append(tempword)
        listnum.append(tempnum)
        tempword = []
        temptag = []
        tempnum = []
    else:
        tempword.append(word[1])
        temptag.append(word[3])
        tempnum.append(word[4])


# print(listtag)
# print(sentence_word_list)
# print(listnum)

#sneha code ends
# print(len(sentence_word_list))
# print(len(label_list))
# print (len(listtag))
listtag.pop()
print(len(sentence_word_list))
print(len(label_list))
print (len(listtag))

for i in range(len(listtag)):
    for j in range(len(listtag[i])):
        if ':' in listtag[i][j]:
            listtag[i][j] = listtag[i][j].split(':')[0]

print(sentence_word_list[19])
print(listtag[19])
print(listnum[19])
# for i in range(len(sentence_word_list)):
#      print(sentence_word_list[i],len(sentence_word_list[i]),len(listtag[i]),len(listnum[i]))

# print(sentence_word_list[14])
# print(listtag[14])
# print(listnum[14])


# rules start here:
for label_index in range(len(label_list)):
    if label_list[label_index]=='SIMILE':
        if 'तरह' in sentence_word_list[label_index]:
            tarah_index = sentence_word_list[label_index].index('तरह')
            if listtag[label_index][tarah_index-1]=='JJ' or listtag[label_index][tarah_index-1]=='QF' or listtag[label_index][tarah_index-1]=='QC' or listtag[label_index][tarah_index-1]=='WQ' or listtag[label_index][tarah_index-1]=='DEM':
                label_list[label_index]='NOT'

        elif 'जैसे' in sentence_word_list[label_index]:
            jaise_index = sentence_word_list[label_index].index('जैसे')
            dependent_jaise_no = int(listnum[label_index][jaise_index])
            dependent_jaise = listtag[label_index][dependent_jaise_no-1]
            if sentence_word_list[label_index][jaise_index+1] == 'ही' or sentence_word_list[label_index][jaise_index+1] == 'की' or sentence_word_list[label_index][jaise_index+1] == 'कि':
                 dependent_ki_hi = int(listnum[label_index][jaise_index+1])
                 if sentence_word_list[label_index][dependent_ki_hi-1]=='जैसे':
                     if listtag[label_index][jaise_index]=='VM' or listnum[label_index][jaise_index]=='0':
                         label_list[label_index]='NOT'
                     elif dependent_jaise=='VM':
                         label_list[label_index] = 'NOT'

        elif 'जैसा' in sentence_word_list[label_index]:
            jaise_index = sentence_word_list[label_index].index('जैसा')
            dependent_jaise_no = int(listnum[label_index][jaise_index])
            dependent_jaise = listtag[label_index][dependent_jaise_no-1]
            if sentence_word_list[label_index][jaise_index+1] == 'ही' or sentence_word_list[label_index][jaise_index+1] == 'की' or sentence_word_list[label_index][jaise_index+1] == 'कि':
                 dependent_ki_hi = int(listnum[label_index][jaise_index+1])
                 if sentence_word_list[label_index][dependent_ki_hi-1]=='जैसा':
                     if listtag[label_index][jaise_index]=='VM' or listnum[label_index][jaise_index]=='0':
                         label_list[label_index]='NOT'
                     elif dependent_jaise=='VM':
                         label_list[label_index] = 'NOT'

        if 'तरह' not in sentence_word_list[label_index] and 'जैसे' not in sentence_word_list[label_index] and 'जैसा' not in sentence_word_list[label_index] and 'जैसी' not in sentence_word_list[label_index]:
            label_list[label_index] = 'NOT'


    elif label_list[label_index]=='NOT':
        if 'तरह' in sentence_word_list[label_index]:
            tarah_index = sentence_word_list[label_index].index('तरह')
            if sentence_word_list[label_index][tarah_index-1]=="की":
                if (listtag[label_index][tarah_index]=='PSP' or listtag[label_index][tarah_index]=='NN') and listtag[label_index][tarah_index-1]=='PSP':
                    dependent_ki_no = int(listnum[label_index][tarah_index-1])
                    dependent_tarah_no = int(listnum[label_index][tarah_index])
                    if dependent_ki_no == dependent_tarah_no and (listtag[label_index][dependent_tarah_no-1]=='NN' or listtag[label_index][dependent_tarah_no-1]=='NNP'):
                        vm_no = int(listnum[label_index][dependent_tarah_no-1])
                        if listtag[label_index][vm_no-1]=='VM':
                            label_list[label_index]='SIMILE'
                            print(label_index)
                        elif vm_no==0:
                            label_list[label_index]='SIMILE'

                if listtag[label_index][tarah_index]=='NN' and listtag[label_index][tarah_index-1]=='PSP':
                    dependent_ki_no = int(listnum[label_index][tarah_index - 1])
                    dependent_tarah_no = int(listnum[label_index][tarah_index])
                    if listtag[label_index][dependent_ki_no-1]=='NN' and (dependent_tarah_no==0 or listtag[label_index][dependent_tarah_no-1]=='VM' or listtag[label_index][dependent_tarah_no-1]=='VAUX'):
                        label_list[label_index]='SIMILE'

        if 'जैसा' in sentence_word_list[label_index]:
            jaisa_index = sentence_word_list[label_index].index('जैसा')
            if sentence_word_list[label_index][jaisa_index+1]=='है' or sentence_word_list[label_index][jaisa_index+1]=='था' or sentence_word_list[label_index][jaisa_index+1]=='थी':
                label_list[label_index]='SIMILE'


        if 'जैसी' in sentence_word_list[label_index]:
            jaisi_index = sentence_word_list[label_index].index('जैसी')
            if sentence_word_list[label_index][jaisi_index + 1] == 'है' or sentence_word_list[label_index][jaisi_index + 1] == 'था' or sentence_word_list[label_index][jaisi_index + 1] == 'थी':
                label_list[label_index] = 'SIMILE'


        elif 'जैसे' in sentence_word_list[label_index] or 'जैसी' in sentence_word_list[label_index] or 'जैसा' in sentence_word_list[label_index]:
            if 'वैसे' in sentence_word_list[label_index] or 'ऐसे' in sentence_word_list[label_index] or 'वैसा' in sentence_word_list[label_index] or 'ऐसा' in sentence_word_list[label_index] or 'ऐसी' in sentence_word_list[label_index] or 'वैसी' in sentence_word_list[label_index]:
                label_list[label_index]='SIMILE'

#to be done after all rules have been written
for label in label_list:
    output_final_file.write(str(label))
    output_final_file.write('\n')

