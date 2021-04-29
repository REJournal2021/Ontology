# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 16:50:15 2020

@author: Murtuza
"""

import pickle
pickle_off = open("final_unique_words_to_consider","rb")
words230 = pickle.load(pickle_off)

import pandas as pd
data= pd.read_csv('tweet_df_with_SOPs.csv')

not_giving_triplet_counter=0
sop_to_consider=[]
for ind, row in data.iterrows():
    print(ind)
    sop=row['results_list']
    sop_list=sop.split()
    if len(sop_list)==3 and sop_list[0]!=sop_list[2]:
        if sop_list[0] in words230  and sop_list[2] in words230 and sop_list not in sop_to_consider:
            sop_to_consider.append(sop_list)
    if len(sop_list)!=3:
        not_giving_triplet_counter+=1


# did not use this yet
sop_to_consider_pedestrian=[]
for sop in sop_to_consider:
    if 'pedestrian' in sop[0] or 'pedestrian' in sop[2]:
        sop_to_consider_pedestrian.append(sop)




new_list=[]
for sop in sop_to_consider:
    subject_ = sop[0]
    object_ =sop[2]
    predicate_ = sop[1]
    
    all_predicates=[]
    all_predicates.append(predicate_)
    
    for sop_again in sop_to_consider:
        if subject_ == sop_again[0] or subject_ == sop_again[2]:
            if object_ == sop_again[0] or object_ == sop_again[2]:
                if predicate_ != sop_again[1] and sop_again[1] not in all_predicates :
                    all_predicates.append(sop_again[1])
    
    lst=[]
    lst.append(subject_)
    lst.append(object_)
    lst.append(all_predicates)
    
    new_list.append(lst)



import pandas as pd
df_ = pd.DataFrame(columns=['subject','object','predicates',])

for row in new_list:
    df_ = df_.append({'subject': str(row[0]), 'object':row[1],'predicates':row[2]},ignore_index=True)

df_ = df_.drop_duplicates(subset=['subject','object'], keep="first")

import numpy as np
df_ = df_[~(np.triu(df_.subject.values[:,None] == df_.object.values)).any(0)]


ped_df = df_.loc[(df_['subject'] == 'pedestrian') | (df_['object'] == 'pedestrian')] 

df_.to_csv('all_sops.csv',index=False)

ped_df.to_csv('pedestrian_sops.csv',index=False)
