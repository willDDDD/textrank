# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download()
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
import nltk
import string
import math
import nltk.stem as ns
import heapq

# main function
def textrank_word(t):
    # each vertex with a list of position that it appears in the text
    dic = {}
    
    # vertices
    graph = []
    
    # neighbours of each vertex
    neber = []
    
    # (previous round)value of each vertex corresponding to the certain index in graph list
    value_old = []
    
    #current round(used to calculate error rate)
    value_cur = []
    
    # error rate
    error = []
    
    #replace punctuation by ' '
    t1 = t.maketrans(string.punctuation,' ' * 32)
    t2 = t.translate(t1)
    wordlist = nltk.word_tokenize(t2)
    
    #lowercase
    for i in range(len(wordlist)):
        wordlist[i] = wordlist[i].lower()
    
    # lemmatize all the words
    origin = ns.WordNetLemmatizer()
    wordlist = [origin.lemmatize(x)  for  x  in  wordlist]
        
    for i in range(len(wordlist)):
        #construct graph
        if nltk.pos_tag(wordlist)[i][1] in ['VB','NN','JJ','NNS' ] and wordlist[i] not in nltk.corpus.stopwords.words('english') and wordlist[i] not in graph:
            graph.append(wordlist[i])
        
        #contruct dic
        if nltk.pos_tag(wordlist)[i][1] in ['VB','NN','JJ','NNS'] and wordlist[i] not in nltk.corpus.stopwords.words('english') and wordlist[i] in dic:
            dic[wordlist[i]].append(i)
            continue
        if nltk.pos_tag(wordlist)[i][1] in ['VB','NN','JJ','NNS']and wordlist[i] not in nltk.corpus.stopwords.words('english') and wordlist[i] not in dic:
            dic[wordlist[i]] = [i]
   
    #construct neber and set each vertice with initial value 1
    for i in range(len(graph)):
        neber.append([])
    for i in range(len(graph)):
        value_cur.append(1)
        value_old.append(1)
        error.append(1)
        for j in range(i+1,len(graph)):
            if j in neber[i]:
                continue
            flag = 0
            for m in dic[graph[i]]:
                if flag == 1:
                    break
                for n in dic[graph[j]]:
                    if abs(m-n) <= 2:  #window <= 2
                        neber[i].append(j)
                        neber[j].append(i)
                        flag = 1

    #recurrsive processes
    # d = 0.85, then 1-d = 0.15
    count = 0
    while not checkerror(error):
        value_old = value_cur.copy()
        for i in range(len(graph)):
            sum = 0
            for j in neber[i]:
                sum += value_cur[j] / len(neber[j])
            value_cur[i] = sum * 0.85 + 0.15
        error = cal_error(value_cur, value_old)
        count+=1
    print(count) # record iteration times
    
    #find top words
    result = { }
    r = map(value_cur.index, heapq.nlargest(math.floor(len(graph) / 3), value_cur))
    for i in r:
        result[graph[i]] = value_cur[i]
    return result
    
# check whether each error under the threshold
def checkerror(er):
    flag = 0
    for i in er:
        if i > 0.0001:
            flag = 1
            break
    if flag == 0:
        return True
    else:
        return False

# calculate current error rate
def cal_error(s2, s1):
    t = []
    for i in range(len(s2)):
        t.append(abs(s2[i] - s1[i]))
    return t


r = textrank_word('Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.')
print(r)