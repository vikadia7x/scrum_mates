import pandas as pd
import numpy as np
import ast 
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD, evaluate
import warnings; warnings.simplefilter('ignore')
import pyodbc
import pickle
import h5py
from azure.storage.blob import BlockBlobService, PublicAccess
import os

def process_Output(metaDataLinks):
    metaDataLinks1 = pd.read_hdf('meta_data.h5', 'metaDataLinks')
    metaDataLinks1 = metaDataLinks1.reset_index()
    metaDataLinks = metaDataLinks.reset_index()
    #print(metaDataLinks.head(5))
    titles = metaDataLinks['title']
    indices= pd.Series(metaDataLinks.index, index= metaDataLinks['title'])
    indices1 = pd.Series(metaDataLinks.index, index= metaDataLinks1['title'])
    print("The indices are")
    print(indices)
    print(indices1)
    return indices

def get_recommendations(title, indices, cosine_sim, metaDataLinks):
    print("Opening Pickle file")
    with h5py.File('cosine_sim_f.h5', 'r') as hf:
        cosine_sim_1 = hf['name-of-dataset'][:]
    print(cosine_sim_1)
    print(cosine_sim)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]
    movie_indices = [i[0] for i in sim_scores]
    movies = metaDataLinks.iloc[movie_indices][['title','flag','id','imdb_id','year','popularity']]
    qualified = movies[movies.flag == 1]
    return qualified

def flow():
    indices = process_Output(metaDataLinks)
    movie_titles = ['The Dark Knight','Inception','The Godfather','Pulp Fiction']
    for movie in movie_titles:
        df = get_recommendations(movie, indices, cosine_sim, metaDataLinks).head(10)
        print(df.head(10))
        recommendation = recommendation.append(df)
    #print(recommendation)

if __name__ == '__main__':  
    
    server = ''
    database = ''
    username = ''
    password = ''
    driver='/usr/local/lib/libmsodbcsql.13.dylib'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    account_name = ''
    key = ""
    block_blob_service = BlockBlobService(account_name=account_name, account_key=key)

    local_path=os.getcwd()
    container_name ='quickstartblobs'
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    fullpath_meta_data = local_path + "/" + "meta_data.h5"
    fullpath_cosine_matrix = local_path + "/" + "cosine_sim_f.h5"

    block_blob_service.get_blob_to_path(container_name, "meta_data.h5", full_path_to_file2)
    metaDataLinks1 = pd.read_hdf('meta_data.h5', 'metaDataLinks')

    block_blob_service.get_blob_to_path(container_name, "cosine_sim_f.h5", fullpath_cosine_matrix)
    with h5py.File('cosine_sim_f.h5', 'r') as hf:
        cosine_sim = hf['name-of-dataset'][:]

    print(metaDataLinks1.head(10))
    print(cosine_sim)

    userSelectedMovies = pd.DataFrame()
    query_userselected = "SELECT * FROM [dbo].[showtimefinder_userselectmovies] WHERE isMovieRec = 0"
    for chunk in pd.read_sql_query(query_userselected, cnxn, chunksize=10**4):
        userSelectedMovies = pd.concat([userSelectedMovies, chunk])
        print(userSelectedMovies)
    print(userSelectedMovies.shape)



    flow()
