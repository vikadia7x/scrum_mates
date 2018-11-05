'''
author: Aditya Samant
The following code requests now playing movies from tmdb api and takes the ids that will be used to write to csv file.
Data collected from themoviedb api in accordance with section 4.1 of its Terms of Use: 
CSV file columns and content
i.      adult (bool); 
            ii.     belongs_to_collection (jsonString w/ id, name, poster_path & backdrop_path)
            iii.    budget (float)
            iv.     genre (list: str)
            v.      homepage (url:str)
            vi.     id (int)
            vii.    imdb_id(str)
            viii.   original_language(str)
            ix.     original_title (str)
            x.      overview (str)
            xi.     popularity(float)
            xii.    poster_path (str)
            xiii.   production_companies (list: jsonObj)
            xiv.    production_countries (list: jsonObj)
            xv.     release_date (yyyy-mm-dd)
            xvi.    revenue (float)
            xvii.   runtime (int)
            xviii.  Spoken_Languages (list: jsonObj)
            xix.    Status ('Released/Unreleased')
            xx.     tagline (str)
            xxi.    title (str)
            xxii.   video (bool)
            xxiii.  vote_average(float)
            xxiv.   vote_count(int)
'''
import csv # to create a csv file
import requests # to get info from api
import sys # for exit
import time # to prevent exceeding api limit 
import pyodbc
import pandas as pd # to import dataframe on to a database
import urllib #to pass through exact pyodbc strin
from sqlalchemy import create_engine # to get the python sql file on the


api_key = 'tmdbkey'
server= 'azureserver,port'
user = 'susername'
password = 'password'
dbname = 'dbname'

try:
    # Get all movies currently in theatres in the US according to TMDB
    csvwriter = csv.writer(open("Now_Playing_Movies_Data.csv", "w+")) # write & make it
    # Headers for the column
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
    df = pd.read_csv('Now_Playing_Movies_Data.csv')
    # Export the resultant csv data to the MSSQL database as per documentation in microsoft
    params=urllib.parse.quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';PWD='+password)
    engine = create_engine('mssql+pyodbc:///odbc_connect=%s'%params)
    
    df.to_sql(
        name= "NowPlayingData",
        con=engine,
        if_exists='replace',
        index=False
        )
      
except Exception as err:
    print(err)
    sys.exit(1)

