'''
author: Aditya Samant
The following code requests info on now playing movies from tmdb api and takes the ids that will be used to write to csv file.
Data collected from themoviedb api in accordance with section 4.1 of its Terms of Use: https://www.themoviedb.org/documentation/api/terms-of-use
CSV files columns and content
1. Now_Playing_Movies_Data.csv
            i.      adult (bool); 
            ii.     belongs_to_collection (jsonString w/ id, name, poster_path & backdrop_path)
            iii.    budget (decimal)
            iv.     genre (list: str)
            v.      homepage (url:str)
            vi.     id (int)
            vii.    imdb_id(str)
            viii.   original_language(str)
            ix.     original_title (str)
            x.      overview (str)
            xi.     popularity(decimal)
            xii.    poster_path (str)
            xiii.   production_companies (list: jsonObj)
            xiv.    production_countries (list: jsonObj)
            xv.     release_date (yyyy-mm-dd)
            xvi.    revenue (decimal)
            xvii.   runtime (int)
            xviii.  Spoken_Languages (list: jsonObj)
            xix.    Status ('Released/Unreleased')
            xx.     tagline (str)
            xxi.    title (str)
            xxii.   video (bool)
            xxiii.  vote_average(decimal)
            xxiv.   vote_count(int)
2. NowPlayingLinks.csv
            i.      movieId (int)
            ii.     imdbId  (int)
            iii.    tmdbId  (int)
3. NowPlayingKeywords.csv
            i.      id (int)
            ii.     keywords (list: jsonObj)
4. NowPlayingCredits.csv
            i.      cast (list: jsonObj)
            ii.     crew (list: jsonObj)
            iii.    id   (int)

'''
import csv # to create a csv file
import requests # to get info from api
import sys # for exit
#import sendtoDB
import time # to prevent exceeding api limit
#import pymssql 
#import pyodbc
#import pandas as pd # to import dataframe on to a database
# import urllib #to pass through exact pyodbc strin
#from sqlalchemy import create_engine # to get the python sql file on the
import config as cf
"""
def sendtoDB(host, uid, pwd, db):
    try:
        df_nowPlaying = pd.read_csv('Now_Playing_Movies_Data.csv')
        df_links = pd.read_csv("NowPlayingLinks.csv")
        df_keywords = pd.read_csv("NowPlayingKeywords.csv")
        df_credits = pd.read_csv("NowPlayingCredits.csv")
        
        print(df_nowPlaying.head())
        print(df_links.head())
        print(df_keywords.head())
        print(df_credits.head())
        
        cxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+host+';DATABASE='+dbname+';UID='+uid+';PWD='+pwd)
        cursor = cxn.cursor()
        # drop preexisting tables
        cursor.execute('DROP TABLE IF EXISTS NowPlayingData;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingLinks;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingCredits;')
        cursor.execute('DROP TABLE IF EXISTS NowPlayingKeywords;')

        tableStr = "CREATE TABLE NowPlayingData (adult varchar(10),belongs_to_collection varchar(max),budget int,genres varchar(max),homepage varchar(max),id int,imdb_id varchar(100),original_language char(2),original_title varchar(500),overview varchar(max), popularity float, poster_path varchar(500), production_companies varchar(max), production_countries varchar(max), release_date date, revenue int, runtime varchar(100), spoken_languages varchar(max), status varchar(10), tagline varchar(max), title varchar(200), video varchar(10), vote_average float, vote_count int);"
        cursor.execute(tableStr)
        tableOneStr = "CREATE TABLE NowPlayingLinks(movieId int, imdbId varchar(100), tmdbId int);"
        tableTwoStr = "CREATE TABLE NowPlayingCredits(cast varchar(max), crew varchar(max), id int);"
        tableThreeStr = "CREATE TABLE NowPlayingKeywords(id int, keywords varchar(max));"
        cursor.execute(tableOneStr)
        cursor.execute(tableTwoStr)
        cursor.execute(tableThreeStr)
        insertString = "INSERT INTO NowPlayingData (adult,belongs_to_collection,budget,genres,homepage,id,imdb_id,original_language,original_title,overview,popularity,poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
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
            cursor.execute(insertString, str(row['adult']), str(row['belongs_to_collection']), row['budget'], str(row['genres']), str(row['homepage']), row['id'], str(row['imdb_id']),
                           str(row['original_language']), str(row['original_title']), str(row['overview']), row['popularity'], str(row['poster_path']), str(row['production_companies']),
                           str(row['production_countries']), row['release_date'], row['revenue'], str(row['runtime']), str(row['spoken_languages']), str(row['status']), str(row['tagline']),
                           str(row['title']),str(row['video']), row['vote_average'], row['vote_count'])
        cxn.commit()
        cursor.close()
        cxn.close()
    except Exception as err:
        print("SendtoDB")
        print(err)
        sys.exit(1)

    returnStr = "Everything printed well"
    return returnStr
"""

try:
   
    #  Get all movies currently in theatres in the US according to TMDB
    csvwriter = csv.writer(open("Now_Playing_Movies_Data.csv", "w+")) # write & make it
    csvwriter2 = csv.writer(open("NowPlayingLinks.csv", "w+"))
    csvwriter3 = csv.writer(open("NowPlayingKeywords.csv", "w+"))
    csvwriter4 = csv.writer(open("NowPlayingCredits.csv", "w+"))
    #  Headers for the column
    csvwriter.writerow(["adult", "belongs_to_collection", "budget", "genres", "homepage", "id", "imdb_id", "original_language", "original_title", "overview",	"popularity", "poster_path",
                        "production_companies", "production_countries", "release_date", "revenue", "runtime",	"spoken_languages", "status", "tagline", "title", "video", "vote_average",	
                        "vote_count"])
    csvwriter2.writerow(["movieId", "imdbId", "tmdbId"])
    csvwriter3.writerow(["id", "keywords"])
    csvwriter4.writerow(["cast", "crew", "id"])
    
    api_key = cf.TMDB_API_KEY
    server = cf.DATABASE_HOST_SERVER
    dbname = cf.DATABASE_NAME
    user = cf.DATABASE_USER
    password = cf.DATABASE_PASSWORD
    
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&region=US" # limit region to limit requests taken
    jsonObj = requests.get(url).json()
    dbid = 0 # DB ids for Links Table
    # Get number of pages to request:
    pages = jsonObj['total_pages']
    counter = 1
    
    while(counter <= pages):
        
        if(counter > 1):
            url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&page=" + str(counter)+"&region=US"
            jsonObj = requests.get(url).json()   

        for results in jsonObj['results']:
            urlStr = "https://api.themoviedb.org/3/movie/"
            url2 = urlStr+str(results['id'])+ "?api_key=" + api_key + "&language=en-US"
            url3 = urlStr+str(results['id'])+"/keywords?api_key="+api_key
            url4 = urlStr+str(results['id'])+"/credits?api_key="+api_key
            jsonObj2 = requests.get(url2).json()
            keywordsJson = requests.get(url3).json()
            if(counter%8 == 0):
                time.sleep(10)
            creditsJson = requests.get(url4).json()
            dbid += 1  
            print("DBID", dbid)
            csvwriter.writerow([jsonObj2["adult"], jsonObj2["belongs_to_collection"], jsonObj2["budget"], jsonObj2["genres"], jsonObj2["homepage"], jsonObj2["id"], jsonObj2["imdb_id"], 
                                jsonObj2["original_language"], jsonObj2["original_title"], jsonObj2["overview"], jsonObj2["popularity"], jsonObj2["poster_path"], jsonObj2["production_companies"], 
                                jsonObj2["production_countries"], jsonObj2["release_date"], jsonObj2["revenue"], jsonObj2["runtime"], jsonObj2["spoken_languages"], jsonObj2["status"], 
                                jsonObj2["tagline"], jsonObj2["title"], jsonObj2["video"], jsonObj2["vote_average"], jsonObj2["vote_count"]])
            csvwriter2.writerow([dbid, jsonObj2["imdb_id"], jsonObj2["id"]])
            csvwriter3.writerow([keywordsJson["id"], keywordsJson["keywords"]])
            csvwriter4.writerow([creditsJson["cast"], creditsJson["crew"], creditsJson["id"]]) 
            print("One") 
        print("finished")
        counter += 1
 
   # print(sendtoDB.sendtoMSSQL(server, dbname,user,password))
    ''' Alternative Ways of Executing 
    df = pd.read_csv('Now_Playing_Movies_Data.csv')
    # Export the resultant csv data to the MSSQL database as per documentation in microsoft
    params=urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';PWD='+password)
    engine = create_engine('mssql+pyodbc:///odbc_connect=%s'%params)
    # engine = create_engine('mssql+pymssql://'+user+':'+password+'@'+server+':'+port+'/'+dbname)
    df.to_sql(
        name= "NowPlayingData",
        con=engine,
        if_exists='replace',
        index=False
    )
    '''
except requests.exceptions.HTTPError as err:
    print("Main method")
    print(err)
    sys.exit(1)