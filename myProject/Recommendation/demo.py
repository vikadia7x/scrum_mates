import pandas as pd
import numpy as np
import ast 
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import pyodbc
import h5py
from azure.storage.blob import BlockBlobService, PublicAccess
import os

metaData = pd.read_excel('processMetadata.xlsx')
metaData['final'] = metaData['genres'] + metaData['keywords'] + metaData['cast'] + metaData['director'] + metaData['description']

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(metaData['final'].values.astype('U'))
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)
print(type(cosine_sim))
print(cosine_sim)