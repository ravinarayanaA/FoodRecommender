import math
import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score



def search(word,j):

	temp1 =[]
	
	f = open("/home/ravinarayana/Desktop/docs/food.txt", "r")				#Food list with ingredients
	searchlines = list(f.readlines())
	f.close()

	for i, line in enumerate(searchlines):									#Finding ingredients of food items
		if i == len(searchlines)-1:
			return [],j	
		word = str(word).lower()
		line = line.lower()
		if word in line:
			del temp1[:]
			j = j+1
			for l in searchlines[i+2:i+100]: 
				if "*" in l:
					break
				temp1.append(l.rstrip('\n\r\t')) 		
			return temp1,j


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(iter_no=0)														#Static variable for counting function call
def find_similarity(folder,keyword_set):

	similarity = []
	del similarity[:]
	find_similarity.iter_no = find_similarity.iter_no + 1
	match_count = 0
	if folder == '':
		folder = str(folder) + "/"	
		cluster_folder = str(folder) * (find_similarity.iter_no - 1)	
		path = "/home/ravinarayana/Desktop/clusters/"+ cluster_folder 
		num_clusters = len(glob.glob1(path,"cluster*.txt"))					#Finding total number of clusters in the folder
	else:
		num_clusters = len(glob.glob1(folder,"cluster*.txt"))
	for k in range (num_clusters):
		if find_similarity.iter_no == 1:
			path = "/home/ravinarayana/Desktop/clusters/"+ cluster_folder + "cluster" + str(k) + ".txt"
		else:
			path = "/home/ravinarayana/Desktop/clusters/" + "cluster" + str(k) + ".txt"	#path for top keywords of cluster
		match_count = 0
		for keyword in keyword_set:
					
			f = open(path, "r")
			keywords = f.readlines()
			f.close()
			cluster_keyword_set = []
			for line in keywords:											#forming of Keyword set of cluster
				cluster_keyword_set.append(line.rstrip('\n'))			
			for doc_word in cluster_keyword_set:
				sim_keyword = JNLA( keyword, doc_word)
				if(sim_keyword > 0.8):										#comparing keyword similarity
					match_count = match_count + 1							#counting matched keywords
		max_val = max( len(keyword_set), len(cluster_keyword_set)) 			#maximum length of 2 sets
		sim_val = float(float(match_count)/float(max_val))					#document similarity
		similarity.append(sim_val)
	return similarity

def ngrams(sequence, n):
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)] 

def distance_bigrams_same(t1, t2):
    t1_terms = list(t1)
    t2_terms = list(t2)
    terms1 = ngrams(t1_terms, 2)
    terms2 = ngrams(t2_terms, 2)
    shared_terms = set(terms1).intersection(terms2)
    all_terms = set(terms1).union(terms2)
    dist = 0.0
    if len(all_terms) > 0:
        dist = (len(shared_terms) / float(len(all_terms)))
    return dist

def hlength(a,b):
	return math.exp( (-abs(len(a)-len(b))/(len(a)+len(b) )))
	    
def jaccards(a,b):
	c = set(a).intersection(b)
	return (float(len(c)) / (len(a) + len(b) - len(c)))

def JNLA(keyword, doc_word):
	jac = jaccards(keyword, doc_word)
	ngram_sim = distance_bigrams_same(keyword, doc_word)
	hlen = hlength(keyword, doc_word)
	#print jac
	#print ngram_sim
	#print hlen
	return ((float(jac)+float(ngram_sim)+float(hlen))/3)
	
def find_items(input_list ):
	output = []
	temp = []
	cluster_labels = []
	cluster_labels.append([])
	documents = []
	keyword_set =[]	
	items = []
	j = 0

	cluster_folder = ''

	var = 1
	while var == 1:
		if j == len(input_list):
		  	var = 0
		else:
			word = str(input_list[j])												#taking every item given as input
			temp1,j = search(input_list[j],j)
			if temp1 == []:															#required document does not exists
				return word + " does not exists"
			documents.append(' '.join(temp1))

	true_k = 1

	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(documents)											#vectorising input food ingredients

	model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=50)
	model.fit(X)																	#calling kmeans function with vectorised data as input
	model_lab = list(model.labels_)													#labels of respective cluster
	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names()
	for i in range(true_k):
		#print "Cluster %d:" % i,   
		for ind in order_centroids[i, :20]:
			#print '%s' % terms[ind],
			keyword_set.append(terms[ind])
	
	similarity = find_similarity('',keyword_set)									#finding similarity for the first time	
	MaxSimCluster = similarity.index(max(similarity))

	folder = str(MaxSimCluster) + "/"
	path = "/home/ravinarayana/Desktop/clusters/"+ folder + str(MaxSimCluster) + ".txt"
	file_path = "/home/ravinarayana/Desktop/clusters/"+ folder
	
	total = 0
	for line in open(path).xreadlines(  ): total += 1
	
	val = 1
	while val == 1: 	
		if (total > 20):
			similarity = find_similarity(file_path,keyword_set)
			#print similarity
			MaxSimCluster = similarity.index(max(similarity))						#most similar cluster
			folder = folder + str(MaxSimCluster) + "/"
			path = "/home/ravinarayana/Desktop/clusters/"+ folder + str(MaxSimCluster) + ".txt"	#Most similar cluster items
			file_path = "/home/ravinarayana/Desktop/clusters/"+ folder				#Most similar cluster path
			
			total = 0
			for line in open(path).xreadlines(  ): total += 1						#finding total number of items in the cluster
		else:	
			f = open(path, "r")
			output = f.readlines()
			for i in output:
				 items.append(i.rstrip('\n'))
			val = 0
	return items

#print(find_items(["rava ladoo", "rasmalai"]))
