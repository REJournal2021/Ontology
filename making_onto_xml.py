# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:44:35 2020

@author: Murtuza
"""

import pandas as pd

data= pd.read_csv('all_sops.csv')

be_words= ['be', 'am', 'is', 'are', 'was', 'were', 'been', 'being',"'s", "’s","’re",'ld','dh','re','fuck','fucked']


for index, row in data.iterrows():
    row['subject'] = row['subject'].capitalize()
    row['object'] = row['object'].capitalize()
    preds= eval(row['predicates'])
    row['predicates']=[x for x in preds if x not in be_words]


data = data[data['predicates'].map(len) != 0]

data.reset_index(inplace=True)
data.drop("index", axis=1, inplace=True)


'''
for filtering predicates -- start

taking top 5 common words based on similarity from Google News and Wikipedia word2vec similarity scores
'''



# using gensim for google news
import gensim
googlew2v = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

import gensim.downloader as api
wikiw2v = api.load("glove-wiki-gigaword-100") 

import operator
import math

import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 

# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()


filtered_preds=[]
for index, row in data.iterrows():
    final_list=[]
    preds= eval(str(row['predicates']))
    
    if len(preds)>5:
        sub_dict_google={}
        obj_dict_google={}
        sub_dict_wiki={}
        obj_dict_wiki={}
        for x in preds:
            try:
                sub_dict_google[x]=googlew2v.similarity(row['subject'],x)
                obj_dict_google[x]=googlew2v.similarity(row['object'],x)
                sub_dict_wiki[x]=wikiw2v.similarity((str(row['subject'])).lower(),x)
                obj_dict_wiki[x]=wikiw2v.similarity(str(row['object']).lower(),x)
            except:
                continue
        sub_dict_google=sorted(sub_dict_google.items(),key=operator.itemgetter(1),reverse=True)
        obj_dict_google=sorted(obj_dict_google.items(),key=operator.itemgetter(1),reverse=True)
        sub_dict_wiki=sorted(sub_dict_wiki.items(),key=operator.itemgetter(1),reverse=True)
        obj_dict_wiki=sorted(obj_dict_wiki.items(),key=operator.itemgetter(1),reverse=True)
        
        
        sub_words_desc_google = [val[0] for val in sub_dict_google]
        obj_words_desc_google = [val[0] for val in obj_dict_google]
        sub_words_desc_wiki = [val[0] for val in sub_dict_wiki]
        obj_words_desc_wiki = [val[0] for val in obj_dict_wiki]
        
        if len(sub_words_desc_google)>20:
            sub_words_desc_google = sub_words_desc_google[:math.ceil((len(sub_words_desc_google)/4))]
    
        if len(obj_words_desc_google)>20:
            obj_words_desc_google = obj_words_desc_google[:math.ceil((len(obj_words_desc_google)/4))]
    
        if len(sub_words_desc_wiki)>20:
            sub_words_desc_wiki = sub_words_desc_wiki[:math.ceil((len(sub_words_desc_wiki)/4))]
    
        if len(obj_words_desc_wiki)>20:
            obj_words_desc_wiki = obj_words_desc_wiki[:math.ceil((len(obj_words_desc_wiki)/4))]
        
        #if len(sub_words_desc_google)>5 or len(obj_words_desc_google)>5 or len(sub_words_desc_wiki)>5 or len(obj_words_desc_wiki)>5:
        s1=set(sub_words_desc_google)
        s2=set(obj_words_desc_google)
        s3=set(sub_words_desc_wiki)
        s4=set(obj_words_desc_wiki)
        set1 = s1.intersection(s2)
        set2 = s3.intersection(s4)
        result_set = set1.intersection(set2)
        final_list = list(result_set)
        final_list = [lemmatizer.lemmatize(val) for val in final_list]
        if len(final_list)>10:
            final_list=final_list[:10]
    else:
        final_list = preds
    filtered_preds.append(final_list)




data = data.assign(filtered_preds=filtered_preds)

data = data[data['filtered_preds'].map(len) != 0]



'''
for filtering predicates -- end
'''









all_classes_for_onto=[]
all_obj_properties_for_onto=[]
for index, row in data.iterrows():
    all_classes_for_onto.append(row['subject'])
    all_classes_for_onto.append(row['object'])
    # if there is no filtering, change filtered_preds to predicates for all predicates
    preds= eval(str(row['filtered_preds']))
    for x in preds:
        all_obj_properties_for_onto.append(x)




all_classes_for_onto = list(set(all_classes_for_onto))
all_obj_properties_for_onto=list(set(all_obj_properties_for_onto))




classes_xml=[]
def make_classes(cls_name):
    start = str('\t<owl:Class rdf:about="http://www.semanticweb.org/murtuza/ontologies/2020/6/sample.owl#')
    end= cls_name + '"/>\n\n\n'
    classes_xml.append( start+end)

for words in all_classes_for_onto:
    make_classes(words)

full_classes=''.join(classes_xml)





obj_prop_xml=[]
def make_obj_prop(dom,prop,ran):
    start= str('\t<owl:ObjectProperty rdf:about="http://www.semanticweb.org/murtuza/ontologies/2020/6/sample.owl#')
    pr = prop + '">\n\t\t'
    dm1 = str('<rdfs:domain rdf:resource="http://www.semanticweb.org/murtuza/ontologies/2020/6/sample.owl#')
    dm2 = dom + '"/>\n\t\t'
    rn1 = str('<rdfs:range rdf:resource="http://www.semanticweb.org/murtuza/ontologies/2020/6/sample.owl#')
    rn2 = ran + '"/>\n\t'
    end = str('</owl:ObjectProperty>\n\n\n')
    obj_prop_xml.append(start+pr+dm1+dm2+rn1+rn2+end)
    

for index, row in data.iterrows():
    # if there is no filtering, change filtered_preds to predicates for all predicates
    preds= eval(str(row['filtered_preds']))
    for x in preds:
        make_obj_prop(row['subject'],x,row['object'])


full_prop=''.join(obj_prop_xml)

