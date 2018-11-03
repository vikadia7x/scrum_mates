import matplotlib.pyplot as plt
import seaborn as sns
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


def preProcess(credits,keywords,links,metaData,ratings):
    metaData['year'] = pd.to_datetime(metaData['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    metaData['year'].replace({'NaT': '0000'}, inplace=True)
    metaData[['year']] = metaData[['year']].astype(int)
    metaData['flag'] = metaData['year'].apply(lambda x: 1 if x > 2015 else 0)
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
    metaDataLinks['cast'] = metaDataLinks['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)
    metaDataLinks['director'] = metaDataLinks['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
    metaDataLinks['director'] = metaDataLinks['director'].apply(lambda x: [x,x, x])
    #s = metaDataLinks.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
    #s = s.value_counts()
    #s = s[s > 1]
    stemmer = SnowballStemmer('english')
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    #metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(filter_keywords)
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    metaDataLinks['keywords'] = metaDataLinks['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    metaDataLinks['keywords'] = metaDataLinks['keywords'].astype(str)
    metaDataLinks['cast'] = metaDataLinks['cast'].astype(str)
    metaDataLinks['director'] = metaDataLinks['director'].astype(str)
    metaDataLinks['genres'] = metaDataLinks['genres'].astype(str)
    metaDataLinks['soup'] = metaDataLinks['keywords'] + metaDataLinks['cast'] + metaDataLinks['director'] + metaDataLinks['genres']
    metaDataLinks['soup'] = metaDataLinks['soup'].apply(lambda x: ' '.join(x))
    metaDataLinks['tagline'] = metaDataLinks['tagline'].fillna('')
    metaDataLinks['description'] = metaDataLinks['overview'] + metaDataLinks['tagline']
    metaDataLinks['description'] = metaDataLinks['description'].fillna('')['description'] = metaDataLinks['description'].fillna('')
    metaDataLinks['final'] = metaDataLinks['soup'] + metaDataLinks['description']
    metaDataLinks = metaDataLinks.drop_duplicates(subset=['title'], keep='first')
    return metaDataLinks


def filtering(metaDataLinks):
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(metaDataLinks['final'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return(cosine_sim)

def process_Output(metaDataLinks):
    metaDataLinks = metaDataLinks.reset_index()
    titles = metaDataLinks['title']
    indices= pd.Series(metaDataLinks.index, index= metaDataLinks['title'])
    return indices

def get_recommendations(title, indices, cosine_sim, metaDataLinks):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]
    movie_indices = [i[0] for i in sim_scores]
    movies = metaDataLinks.iloc[movie_indices][['title','flag','id','imdb_id','year','popularity']]
    qualified = movies[movies.flag == 1]
    return qualified


def flow():
    recommendation = pd.DataFrame()
    metaDataLinks = preProcess(credits,keywords,links,metaData,ratings)
    cosine_sim = filtering(metaDataLinks)
    indices = process_Output(metaDataLinks)
    movie_titles = ['The Dark Knight','Inception','Pulp Fiction','Interstellar','Marley & Me']
    for movie in movie_titles:
        df = get_recommendations(movie, indices, cosine_sim, metaDataLinks).head(10)
        recommendation = recommendation.append(df)

if __name__ == '__main__':  
    credits = pd.read_csv('test_data/credits.csv')
    keywords = pd.read_csv('test_data/keywords.csv')
    links = pd.read_csv('test_data/links.csv')
    metaData = pd.read_csv('test_data/metaDataPreprocessed.csv')
    ratings = pd.read_csv('test_data/ratings_small.csv')

    flow()
