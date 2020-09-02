from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def extract_text(dct):
    res = []
    
    if 'text' in dct:
        res.append(dct['text'].strip())
        
    if dct['children']:
        for x in dct['children']:
            res.append(extractText(x))
    
    return res


def get_bigrams(word, bow='<', eow='>'):
    
    bigramlist = set()
    #print(word)
    charlist = [ch for ch in word if ch.isalpha()]
    #print(len(charlist))
    
    if len(charlist)==0:
        return str([bow+eow])
        
    bigramlist.add(bow+charlist[0])
    for i in range (len(charlist)-1):
        if charlist[i].isalpha():
            bigram = charlist[i] + charlist[i+1]
            bigramlist.add(bigram);
    bigramlist.add(charlist[len(charlist)-1] + eow)
    return str(list(bigramlist))


def get_most_similar_name(name, names):
    
    names_1 = names.copy()
    names_1.append(name)    
    
    bigram_match_names=[]
    for name in names_1:
        bigram_match_names.append(get_bigrams(name))
        
    vector_match_names=[]
    CV = CountVectorizer()
    X = CV.fit_transform(bigram_match_names)
    for i in X:
        vector_match_names.append(i.toarray())
    
    vectors=[x[0] for x in vector_match_names]
    vectors_1 = vectors.copy()
    
    x = vectors_1.pop(names_1.index(name))
    names_1.pop(names_1.index(name))
    
    res=cosine_similarity(x.reshape(1, -1), vectors_1)[0]
    name_sim_dict=dict(zip(names_1,res))
    list_d = list(name_sim_dict.items())
    list_d.sort(key=lambda i: i[1])

    list_d.sort(key=lambda i: i[1], reverse=True)
    print("Most similar names:")
    for i in range (min(5, len(list_d))):
        print(list_d[i][0], ':', list_d[i][1])
        
    return list_d[0][0]
    
    