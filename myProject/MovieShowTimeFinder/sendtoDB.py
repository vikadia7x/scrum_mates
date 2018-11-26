"""
author: Aditya Samant
Send data from csv files to respective databases via the use of pyodbc and pandas dataframes.
"""
import sys
import pyodbc
import pandas as pd
import config as cf

def sendtoMSSQL(server, dbname, user, password):
    try:
        df_nowPlaying = pd.read_csv('Now_Playing_Movies_Data.csv')
        df_nowPlaying.fillna("")
        #print(df_nowPlaying["tagline"].tail())
        df_links = pd.read_csv("NowPlayingLinks.csv")
        df_keywords = pd.read_csv("NowPlayingKeywords.csv")
        df_credits = pd.read_csv("NowPlayingCredits.csv")
        """
        print(df_nowPlaying.head())
        print(df_links.head())
        print(df_keywords.head())
        print(df_credits.head())
        """
        cxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';PWD='+password)
        cursor = cxn.cursor()
        # drop preexisting tables
        cursor.execute('DROP TABLE IF EXISTS NowPlayingData;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingLinks;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingCredits;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingKeywords;')
        
        tableStr = "CREATE TABLE NowPlayingData (adult varchar(10),belongs_to_collection nvarchar(max),budget int, genres nvarchar(max),homepage nvarchar(500), id int, imdb_id varchar(100), original_language char(2), original_title nvarchar(max), overview nvarchar(max), popularity float, poster_path nvarchar(200), production_companies nvarchar(max), production_countries nvarchar(max), release_date date, revenue int, runtime varchar(10), spoken_languages nvarchar(max), status nvarchar(10), tagline nvarchar(1000), title nvarchar(1000), video varchar(10), vote_average float, vote_count int);"
        cursor.execute(tableStr)
        tableOneStr = "CREATE TABLE NowPlayingLinks(movieId int, imdbId varchar(100), tmdbId int);"
        tableTwoStr = "CREATE TABLE NowPlayingCredits(cast varchar(max), crew varchar(max), id int);"
        tableThreeStr = "CREATE TABLE NowPlayingKeywords(id int, keywords varchar(max));"
        cursor.execute(tableOneStr)
        cursor.execute(tableTwoStr)
        cursor.execute(tableThreeStr)
        insertString = "INSERT INTO NowPlayingData (adult,belongs_to_collection,budget,genres,homepage,id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries,release_date,revenue,runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        
        insertOneString= "INSERT INTO NowPlayingLinks (movieId, imdbId, tmdbId) values(?, ?, ?);"
        insertTwoString= "INSERT INTO NowPlayingCredits(cast, crew, id) values(?, ?, ?);"
        insertThreeString= "INSERT INTO NowPlayingKeywords(id, keywords) values(?, ?);"

        for index, row in df_links.iterrows():
            cursor.execute(insertOneString, str(row['movieId']), str(row['imdbId']),str(row["tmdbId"]))
        cxn.commit()
        print("finished links")
        for index, row in df_keywords.iterrows():
            cursor.execute(insertThreeString, str(row['id']), str(row['keywords']))
        cxn.commit()
        print("finished keywords")
        for index, row in df_credits.iterrows():
            cursor.execute(insertTwoString, str(row['cast']), str(row['crew']), str(row['id']))
        cxn.commit()
        print("finished credits")
        
        for index,row in df_nowPlaying.iterrows():
            cursor.execute(insertString, str(row['adult']), str(row['belongs_to_collection']), row['budget'], str(row['genres']), str(row['homepage']), row['id'], str(row['imdb_id']), str(row['original_language']), str(row['original_title']), str(row['overview']), row['popularity'], str(row['poster_path']), str(row['production_companies']), str(row['production_countries']), row['release_date'], row['revenue'], str(row['runtime']), str(row['spoken_languages']), "Released", str(row["tagline"]), str(row['title']), str(row['video']), row['vote_average'], row['vote_count'])
            
        cxn.commit()
        cursor.close()
        cxn.close()
    except Exception as err:
        print(err)
        sys.exit(1)
    statement = "Everything went well :D"
    return statement

print(sendtoMSSQL(cf.DATABASE_HOST_SERVER, cf.DATABASE_NAME, cf.DATABASE_USER, cf.DATABASE_PASSWORD))