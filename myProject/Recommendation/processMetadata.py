import pyodbc
import pandas as pd
import numpy as np
import ast 
from ast import literal_eval
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

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

def preProcess(metaData, credits, keywords, links):
    print(credits.dtypes)
    print(keywords.dtypes)
    print(links.dtypes)
    print(metaData.dtypes)
    
    metaData['year'] = pd.to_datetime(metaData['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    metaData['year'].replace({'NaT': '0000'}, inplace=True)
    metaData[['year']] = metaData[['year']].astype(int)
    
    metaData['flag'] = 0

    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')
    metaData['id'] = metaData['id'].astype('int')

    links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')

    metaData = metaData.merge(credits, on='id')
    metaData = metaData.merge(keywords, on='id')

    metaDataLinks = metaData[metaData.id.isin(links)]

    metaDataLinks['cast'] = metaDataLinks['cast'].apply(literal_eval)
    metaDataLinks['crew'] = metaDataLinks['crew'].apply(literal_eval)
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(literal_eval)
    metaDataLinks['cast_size'] = metaDataLinks['cast'].apply(lambda x: len(x))
    metaDataLinks['crew_size'] = metaDataLinks['crew'].apply(lambda x: len(x))

    metaDataLinks['director'] = metaDataLinks['crew'].apply(get_director)
    metaDataLinks['cast'] = metaDataLinks['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    metaDataLinks['cast'] = metaDataLinks['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)
    print(metaDataLinks['cast'])
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    metaDataLinks['director'] = metaDataLinks['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
    metaDataLinks['director'] = metaDataLinks['director'].apply(lambda x: [x,x, x])

    print(metaDataLinks.head(10))
    
    
    stemmer = SnowballStemmer('english')
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    
    metaDataLinks['keywords'] = metaDataLinks['keywords'].astype(str)
    metaDataLinks['cast'] = metaDataLinks['cast'].astype(str)
    metaDataLinks['director'] = metaDataLinks['director'].astype(str) 
    metaDataLinks['genres'] = metaDataLinks['genres'].astype(str)

    metaDataLinks['tagline'] = metaDataLinks['tagline'].fillna('')
    metaDataLinks['description'] = metaDataLinks['overview'] + metaDataLinks['tagline']
    metaDataLinks['description'] = metaDataLinks['description'].fillna('')

    metaDataLinks['soup'] = metaDataLinks['genres'] + metaDataLinks['keywords'] + metaDataLinks['cast'] + metaDataLinks['director'] + metaDataLinks['description']
    metaDataLinks['soup'] = metaDataLinks['soup'].apply(lambda x: ' '.join(x))
    
    metaDataLinks = metaDataLinks.drop_duplicates(subset=['title'], keep='first')
    print(metaDataLinks.head(10))

    return metaDataLinks

def flow():
    metaDataLinks = preProcess(metaData, credits, keywords, links)
    print(metaDataLinks.head(10))
    print(metaDataLinks.dtypes)

    writer = pd.ExcelWriter('processMetadata.xlsx')
    metaDataLinks.to_excel(writer,'Sheet1')
    writer.save()

if __name__ == '__main__':  
    
    server = 'showtimefinder.database.windows.net'
    database = 'showtimefinder_db'
    username = 'scrum_mates@showtimefinder'
    password = 'Azure@Cloud'
    driver='/usr/local/lib/libmsodbcsql.13.dylib'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    metaData = pd.DataFrame()
    query_meta = "SELECT CONVERT(int,CONVERT(float,id)) AS id, title, release_date, genres, tagline, overview, imdb_id, popularity, status, vote_average, vote_count FROM [dbo].[movie_metadata] "
    for chunk in pd.read_sql_query(query_meta, cnxn, chunksize=10**4):
        metaData = pd.concat([metaData, chunk])
        print(metaData)
    print(metaData.shape)

    credits = pd.DataFrame()
    query_credits = "SELECT * FROM [dbo].[credits2]"
    for chunk in pd.read_sql_query(query_credits, cnxn, chunksize=10**4):
        credits = pd.concat([credits, chunk])
        print(credits)
    print(credits.shape)

    keywords = pd.DataFrame()
    query_keywords = "SELECT * FROM [dbo].[keywords2]"
    for chunk in pd.read_sql_query(query_keywords, cnxn, chunksize=10**4):
        keywords = pd.concat([keywords, chunk])
        print(keywords)
    print(keywords.shape)

    links = pd.DataFrame()
    query_links = "SELECT movieId, imdbId, CONVERT(int,tmdbId) AS tmdbId FROM [dbo].[links2]"
    for chunk in pd.read_sql_query(query_links, cnxn, chunksize=10**4):
        links = pd.concat([links, chunk])
        print(links)
    print(links.shape)

    flow()
