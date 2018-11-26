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

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

def preProcess(metaData, nowPlayingMetaData, credits_nowplaying, keywords_nowplaying, links_nowplaying):
    print(metaData.dtypes)
    print(nowPlayingMetaData.dtypes)
    print(credits_nowplaying.dtypes)
    print(keywords_nowplaying.dtypes)
    print(links_nowplaying.dtypes)
    
    nowPlayingMetaData['genres'] = nowPlayingMetaData['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    nowPlayingMetaData['year'] = pd.to_datetime(nowPlayingMetaData['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    nowPlayingMetaData['year'].replace({'NaT': '0000'}, inplace=True)
    nowPlayingMetaData[['year']] = nowPlayingMetaData[['year']].astype(int)
    
    nowPlayingMetaData['flag'] = 1

    keywords_nowplaying['id'] = keywords_nowplaying['id'].astype('int')
    credits_nowplaying['id'] = credits_nowplaying['id'].astype('int')
    nowPlayingMetaData['id'] = nowPlayingMetaData['id'].astype('int')

    links_nowplaying = links_nowplaying[links_nowplaying['tmdbId'].notnull()]['tmdbId'].astype('int')

    nowPlayingMetaData = nowPlayingMetaData.merge(credits_nowplaying, on='id')
    nowPlayingMetaData = nowPlayingMetaData.merge(keywords_nowplaying, on='id')

    nowPlayingMetaDataLinks = nowPlayingMetaData[nowPlayingMetaData.id.isin(links_nowplaying)]

    nowPlayingMetaDataLinks['cast'] = nowPlayingMetaDataLinks['cast'].apply(literal_eval)
    nowPlayingMetaDataLinks['crew'] = nowPlayingMetaDataLinks['crew'].apply(literal_eval)
    nowPlayingMetaDataLinks['keywords'] = nowPlayingMetaDataLinks['keywords'].apply(literal_eval)
    nowPlayingMetaDataLinks['cast_size'] = nowPlayingMetaDataLinks['cast'].apply(lambda x: len(x))
    nowPlayingMetaDataLinks['crew_size'] = nowPlayingMetaDataLinks['crew'].apply(lambda x: len(x))
    nowPlayingMetaDataLinks['director'] = nowPlayingMetaDataLinks['crew'].apply(get_director)
    nowPlayingMetaDataLinks['cast'] = nowPlayingMetaDataLinks['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)
    print(nowPlayingMetaDataLinks['cast'])
    nowPlayingMetaDataLinks['director'] = nowPlayingMetaDataLinks['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
    nowPlayingMetaDataLinks['director'] = nowPlayingMetaDataLinks['director'].apply(lambda x: [x,x, x])

    print(nowPlayingMetaDataLinks.head(10))
    
    
    stemmer = SnowballStemmer('english')
    nowPlayingMetaDataLinks['keywords'] = nowPlayingMetaDataLinks['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    nowPlayingMetaDataLinks['keywords'] = nowPlayingMetaDataLinks['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    nowPlayingMetaDataLinks['keywords'] = nowPlayingMetaDataLinks['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    nowPlayingMetaDataLinks['keywords'] = nowPlayingMetaDataLinks['keywords'].astype(str)

    nowPlayingMetaDataLinks['cast'] = nowPlayingMetaDataLinks['cast'].astype(str)

    nowPlayingMetaDataLinks['director'] = nowPlayingMetaDataLinks['director'].astype(str) 

    nowPlayingMetaDataLinks['genres'] = nowPlayingMetaDataLinks['genres'].astype(str)

    nowPlayingMetaDataLinks['tagline'] = nowPlayingMetaDataLinks['tagline'].fillna('')
    nowPlayingMetaDataLinks['description'] = nowPlayingMetaDataLinks['overview'] + nowPlayingMetaDataLinks['tagline']
    nowPlayingMetaDataLinks['description'] = nowPlayingMetaDataLinks['description'].fillna('')

    nowPlayingMetaDataLinks['final'] = nowPlayingMetaDataLinks['genres'] + nowPlayingMetaDataLinks['keywords'] + nowPlayingMetaDataLinks['cast'] + nowPlayingMetaDataLinks['director'] + nowPlayingMetaDataLinks['description']

    print(nowPlayingMetaDataLinks['final'])
    metaData['final'] = metaData['genres'] + metaData['keywords'] + metaData['cast'] + metaData['director'] + metaData['description']
    metaData = metaData[['id', 'title', 'release_date', 'genres', 'tagline', 'overview', 'imdb_id', 'popularity', 'status', 'vote_average', 'vote_count', 'year', 'flag', 'cast', 'crew', 'keywords', 'cast_size', 'crew_size', 'director', 'description', 'final']]
    print(nowPlayingMetaDataLinks.shape)
    print(metaData.shape)
    print(nowPlayingMetaDataLinks.dtypes)
    print(metaData.dtypes)
    metaData = metaData.append(nowPlayingMetaDataLinks)
    print(metaData['final'])
    print(metaData.shape)
    print(metaData.dtypes)

    metaData = metaData.drop_duplicates(subset=['title'], keep='first')
    print(metaData.head(10))

    return metaData

def filtering(metaDataLinks):
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(metaDataLinks['final'].values.astype('U'))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    print(cosine_sim.shape)
    print(type(cosine_sim))
    print(cosine_sim)
    print("Pickling")
    metaDataLinks = metaDataLinks.drop(['release_date', 'genres', 'tagline', 'overview', 'status', 'vote_average', 'vote_count', 'cast', 'crew', 'keywords', 'cast_size', 'crew_size', 'director', 'description', 'final'], axis=1)
    """
    with h5py.File('cosine_sim_f.h5', 'w') as hf:
        hf.create_dataset("name-of-dataset",  data=cosine_sim)"""
    np.save('cosine_sim.npy', cosine_sim)    # .npy extension is added if not given
    print("cosine converted")

    d = np.load('cosine_sim.npy')
    print(d)
    print("cosine shown")
    #metaDataLinks.to_hdf('meta_data.h5', key='metaDataLinks', mode='w')
    #print("metadata converted")

    local_path=os.getcwd()
    container_name ='quickstartblobs'
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    fullpath_meta_data = local_path + "/" + "meta_data.h5"
    fullpath_cosine_matrix = local_path + "/" + "cosine_sim_f.h5"
    #block_blob_service.create_blob_from_path(container_name, "meta_data.h5", fullpath_meta_data)
    #print("meta data added")
    block_blob_service.create_blob_from_path(container_name, "cosine_sim_f.h5", fullpath_cosine_matrix)
    print("cosine added")

    print("Pickling done")

    print("\nList blobs in the container")
    generator = block_blob_service.list_blobs(container_name)
    for blob in generator:
        print("\t Blob name: " + blob.name)


    return(cosine_sim)

def flow():
    metaDataLinks = preProcess(metaData, nowPlayingMetaData, credits_nowplaying, keywords_nowplaying, links_nowplaying)
    cosine_sim = filtering(metaDataLinks)


if __name__ == '__main__':  
    
    
    server = ''
    database = ''
    username = ''
    password = ''
    driver='/usr/local/lib/libmsodbcsql.13.dylib'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    """
    account_name = ''
    key = ""
    block_blob_service = BlockBlobService(account_name=account_name, account_key=key)

    """
    metaData = pd.DataFrame()
    query_meta = "SELECT id, title, release_date, genres, tagline, overview, imdb_id, popularity, status, vote_average, vote_count, year, flag, cast, crew, keywords, cast_size, crew_size, director, description FROM [dbo].[processMetadata] "
    for chunk in pd.read_sql_query(query_meta, cnxn, chunksize=10**4):
        metaData = pd.concat([metaData, chunk])
        print(metaData)
    print(metaData.shape)

    nowPlayingMetaData = pd.DataFrame()
    query_nowmeta = "SELECT CONVERT(int,id) AS id, title, release_date, genres, tagline, overview, imdb_id, popularity, status, vote_average, vote_count FROM [dbo].[NowPlayingData] "
    for chunk in pd.read_sql_query(query_nowmeta, cnxn, chunksize=10**4):
        nowPlayingMetaData = pd.concat([nowPlayingMetaData, chunk])
        print(nowPlayingMetaData)
    print(nowPlayingMetaData.shape)

    credits_nowplaying = pd.DataFrame()
    query_credits = "SELECT * FROM [dbo].[NowPlayingCredits]"
    for chunk in pd.read_sql_query(query_credits, cnxn, chunksize=10**4):
        credits_nowplaying = pd.concat([credits_nowplaying, chunk])
        print(credits_nowplaying)
    print(credits_nowplaying.shape)

    keywords_nowplaying = pd.DataFrame()
    query_keywords = "SELECT * FROM [dbo].[NowPlayingKeywords]"
    for chunk in pd.read_sql_query(query_keywords, cnxn, chunksize=10**4):
        keywords_nowplaying = pd.concat([keywords_nowplaying, chunk])
        print(keywords_nowplaying)
    print(keywords_nowplaying.shape)

    links_nowplaying = pd.DataFrame()
    query_links = "SELECT movieId, imdbId, CONVERT(int,tmdbId) AS tmdbId FROM [dbo].[NowPlayingLinks]"
    for chunk in pd.read_sql_query(query_links, cnxn, chunksize=10**4):
        links_nowplaying = pd.concat([links_nowplaying, chunk])
        print(links_nowplaying)
    print(links_nowplaying.shape)

    userSelectedMovies = pd.DataFrame()
    query_userselected = "SELECT * FROM [dbo].[showtimefinder_userselectmovies] WHERE isMovieRec = 0"
    for chunk in pd.read_sql_query(query_userselected, cnxn, chunksize=10**4):
        userSelectedMovies = pd.concat([userSelectedMovies, chunk])
        print(userSelectedMovies)
    print(userSelectedMovies.shape)

    flow()
