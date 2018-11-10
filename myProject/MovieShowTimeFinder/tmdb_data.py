'''
author: Aditya Samant
The following code requests now playing movies from tmdb api and takes the ids that will be used to write to csv file.
Data collected from themoviedb api in accordance with section 4.1 of its Terms of Use: 
CSV file columns and content
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
'''
import csv # to create a csv file
import requests # to get info from api
import sys # for exit
import time # to prevent exceeding api limit
#import pymssql 
import pyodbc
import pandas as pd # to import dataframe on to a database
# import urllib #to pass through exact pyodbc strin
#from sqlalchemy import create_engine # to get the python sql file on the


api_key = 'ce4ca93f8fa013d449e34523c2aff0bb'
server= 'showtimefinder.database.windows.net'
port = '1433'
user = 'scrum_mates@showtimefinder'
password = 'Azure@Cloud'
dbname = 'showtimefinder_db'

def sendtoMSSQL(host, uid, pwd, db):
    try:
            # get data make it into a pandas dataframe
        df = pd.read_csv('Now_Playing_Movies_Data.csv')
        cxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+host+';DATABASE='+dbname+';UID='+uid+';PWD='+pwd)
        cursor = cxn.cursor()
        cursor.execute('DROP TABLE IF EXISTS NowPlayingData;')
        cxn.commit()
        tableStr = "CREATE TABLE NowPlayingData (adult varchar(100), belongs_to_collection varchar(max), budget varchar(100), genres varchar(max), homepage varchar(max), id varchar(100), imdb_id varchar(100), original_language char(100), original_title varchar(max), overview varchar(max), popularity varchar(100), poster_path varchar(max), production_companies varchar(max), production_countries varchar(max), release_date varchar(100), revenue varchar(100), runtime varchar(100), spoken_languages varchar(max), status varchar(100), tagline varchar(max), title varchar(max) , video varchar(100), vote_average varchar(100), vote_count varchar(100));"
        cursor.execute(tableStr)
        cxn.commit()
        insertString = "INSERT INTO NowPlayingData (adult, belongs_to_collection, budget, genres, homepage, id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        
        for index,row in df.iterrows():
            cursor.execute(insertString, str(row['adult']), str(row['belongs_to_collection']), str(row['budget']), str(row['genres']),str(row['homepage']), str(row['id']), str(row['imdb_id']), 
                           str(row['original_language']), str(row['original_title']), str(row['overview']), str(row['popularity']), str(row['poster_path']), str(row['production_companies']),
                           str(row['production_countries']), str(row['release_date']), str(row['revenue']), str(row['runtime']), str(row['spoken_languages']), str(row['status']), 
                           str(row['tagline']), str(row['title']), str(row['video']), str(row['vote_average']), str(row['vote_count']))
            cxn.commit()
        cursor.close()
        cxn.close()
    except Exception as err:
        print(err)
        sys.exit(1)
    
    returnStr = "Everything printed well"
    return returnStr

try:
   
    #  Get all movies currently in theatres in the US according to TMDB
    csvwriter = csv.writer(open("Now_Playing_Movies_Data.csv", "w+")) # write & make it
    #  Headers for the column
    csvwriter.writerow(["adult", "belongs_to_collection", "budget", "genres", "homepage", "id", "imdb_id", "original_language", "original_title", "overview",	"popularity", "poster_path",
                        "production_companies", "production_countries", "release_date", "revenue", "runtime",	"spoken_languages", "status", "tagline", "title", "video", "vote_average",	
                        "vote_count"])
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&region=US" # limit region to limit requests taken
    res = requests.get(url)
    jsonObj = res.json()

    # Get number of pages to request:
    pages = jsonObj['total_pages']
    counter = 1
    while(counter <= pages):
        if(counter > 1):
            url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&page=" + str(counter)+"&region=US"
            res = requests.get(url)
            jsonObj = res.json()

        if(counter%2 != 0):
            print("Delay hit")
            time.sleep(10) # sleep for 10 seconds if the page is an even number
        
        for results in jsonObj['results']:
            url2 = "https://api.themoviedb.org/3/movie/"+str(results['id'])+ "?api_key=" + api_key + "&language=en-US"
            res2 = requests.get(url2)
            jsonObj2 = res2.json()
            csvwriter.writerow([jsonObj2["adult"], jsonObj2["belongs_to_collection"], jsonObj2["budget"], jsonObj2["genres"], jsonObj2["homepage"], jsonObj2["id"], jsonObj2["imdb_id"], 
                                jsonObj2["original_language"], jsonObj2["original_title"], jsonObj2["overview"], jsonObj2["popularity"], jsonObj2["poster_path"], jsonObj2["production_companies"], 
                                jsonObj2["production_countries"], jsonObj2["release_date"], jsonObj2["revenue"], jsonObj2["runtime"], jsonObj2["spoken_languages"], jsonObj2["status"], 
                                jsonObj2["tagline"], jsonObj2["title"], jsonObj2["video"], jsonObj2["vote_average"], jsonObj2["vote_count"]])
            
        print("finished :)")
        counter += 1  

    print(sendtoMSSQL(server, user, password, dbname))

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
    print(err)
    sys.exit(1)

