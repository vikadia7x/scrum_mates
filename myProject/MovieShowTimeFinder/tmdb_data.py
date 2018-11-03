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
# import pymssql # to get the 
import pyodbc
import pandas as pd # to import dataframe on to a database

api_key = 'ce4ca93f8fa013d449e34523c2aff0bb'
server= 'showtimefinder.database.windows.net,1433'
user = 'scrum_mates@showtimefinder'
password = 'Azure@Cloud'
dbname = 'showtimefinder_db'
def upload_data(server, user, password, dbname):
    df = pd.read_csv('Now_Playing_Movies_Data.csv', sep=',', na_values=())
    print(df.head())
    # Export the resultant csv data to the MSSQL database as per documentation in microsoft
    try:
        cxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';PWD='+password)
        cursor = cxn.cursor()

        # create a table
        cursor.execute('DROP TABLE IF EXISTS NowPlayingData;') #Drop table if it is there already
        cr_table = """CREATE TABLE NowPlayingData(adult VARCHAR(6), belongs_to_collection VARCHAR(255), budget MONEY, genres VARCHAR(255), homepage VARCHAR(255), id INT, imdb_id VARCHAR(50), 
                    original_language CHAR(2), original_title VARCHAR(255), overview VARCHAR(500),popularity VARCHAR(255),poster_path VARCHAR(255), production_companies VARCHAR(500), 
                    production_countries VARCHAR(1000), release_date DATE, revenue MONEY, runtime INT, spoken_languages VARCHAR(255),status VARCHAR(8), tagline VARCHAR(255), 
                    title VARCHAR(255),video VARCHAR(255), vote_average DECIMAL(5,2),vote_count INT);"""
        #a= 
        cursor.execute(cr_table)
        cxn.commit()
        #for b in a:
         #   print(b)
        #print(a)
        # iterrate through dataframe while inserting into the table
        for index, row in df.iterrows():
            cursor.execute('''INSERT INTO NowPlayingData([adult], [belongs_to_collection], [budget], [genres], [homepage], [id], [imdb_id], [original_language], 
                        [original_title],[overview],[popularity], [poster_path], [production_companies], [production_countries], [release_date],[revenue], 
                        [runtime], [spoken_languages], [status], [tagline],[title], [video], [vote_average],[vote_count]) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', row["adult"], row["belongs_to_collection"], 
                        row["budget"], row["genres"], row["homepage"], row["id"], row["imdb_id"], row["original_language"], row["original_title"], 
                        row["overview"], row["popularity"], row["poster_path"], row["production_companies"], row["production_countries"], 
                        row["release_date"], row["revenue"], row["runtime"], row["spoken_languages"], row["status"], row["tagline"], row["title"], 
                        row["video"], row["vote_average"], row["vote_count"])
        cxn.commit()
        cursor.close()
        cxn.close()
    except Exception as err:
        print(err)
        sys.exit(1)
    str = "successfully completed insertion"
    return str

try:
    '''
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
    '''    
    print(upload_data(server, user, password, dbname))
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

