import csv # to create a csv file
import requests # to get info from api
import sys # for exit
import time # to prevent exceeding api limit
import pyodbc
import config as cf
# start = time.time()
# f = open("/home/ubuntu/text.txt", "w")
try:
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
    cxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+dbname+';UID='+user+';PWD='+password)
    cursor = cxn.cursor()
    cursor.execute('DROP TABLE IF EXISTS NowPlayingData;')
    cursor.execute('DROP TABLE IF EXISTS NowPlayingLinks;')
    cursor.execute('DROP TABLE IF EXISTS NowPlayingCredits;')
    cursor.execute('DROP TABLE IF EXISTS NowPlayingKeywords;')
    
    tableStr = "CREATE TABLE NowPlayingData (adult nvarchar(10),belongs_to_collection nvarchar(max),budget int, genres nvarchar(max),homepage nvarchar(500), id int, imdb_id nvarchar(100), original_language char(2), original_title nvarchar(max), overview nvarchar(max), popularity float, poster_path nvarchar(200), production_companies nvarchar(max), production_countries nvarchar(max), release_date date, revenue int, runtime varchar(10), spoken_languages nvarchar(max), status nvarchar(10), tagline nvarchar(1000), title nvarchar(1000), video varchar(10), vote_average float, vote_count int);" 
    cursor.execute(tableStr)
    tableOneStr = "CREATE TABLE NowPlayingLinks (movieId int, imdbId varchar(100), tmdbId int);"
    tableTwoStr = "CREATE TABLE NowPlayingCredits (cast nvarchar(max), crew nvarchar(max), id int);"
    tableThreeStr = "CREATE TABLE NowPlayingKeywords (id int, keywords varchar(max));"
    cursor.execute(tableOneStr)
    cursor.execute(tableTwoStr)
    cursor.execute(tableThreeStr)
    insertString = "INSERT INTO NowPlayingData (adult,belongs_to_collection,budget,genres,homepage,id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries,release_date,revenue, runtime,spoken_languages, status, tagline, title, video, vote_average, vote_count) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        
    insertOneString= "INSERT INTO NowPlayingLinks (movieId, imdbId, tmdbId) values(?, ?, ?);"
    insertTwoString= "INSERT INTO NowPlayingCredits (cast, crew, id) values(?, ?, ?);"
    insertThreeString= "INSERT INTO NowPlayingKeywords (id, keywords) values(?, ?);"

    reqs = 0
    while(counter <= pages):
        
        if(counter > 1):
            if(reqs >=39):
                time.sleep(10)
                reqs = 1
                url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&page=" + str(counter)+"&region=US"
            else:
                reqs +=1
                url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&page=" + str(counter)+"&region=US"
            jsonObj = requests.get(url).json()   

        for results in jsonObj['results']:
            if(reqs >=37):
                # print(reqs)
                reqs = 3
                time.sleep(10)
                urlStr = "https://api.themoviedb.org/3/movie/"
                url2 = urlStr+str(results['id'])+ "?api_key=" + api_key + "&language=en-US"
                url3 = urlStr+str(results['id'])+"/keywords?api_key="+api_key
                url4 = urlStr+str(results['id'])+"/credits?api_key="+api_key
            else:
                urlStr = "https://api.themoviedb.org/3/movie/"
                url2 = urlStr+str(results['id'])+ "?api_key=" + api_key + "&language=en-US"
                url3 = urlStr+str(results['id'])+"/keywords?api_key="+api_key
                url4 = urlStr+str(results['id'])+"/credits?api_key="+api_key
                reqs+=3
                
            
            jsonObj2 = requests.get(url2).json()
            keywordsJson = requests.get(url3).json()
            creditsJson = requests.get(url4).json()
            dbid += 1  
            # print("DBID", dbid)
            # print("reached1")
            cursor.execute(insertOneString, dbid, str(jsonObj2['imdb_id']),jsonObj2['id'])
            # print("links")
            cursor.execute(insertThreeString, keywordsJson["id"], str(keywordsJson["keywords"]))
            # print("keywords") 
            cursor.execute(insertTwoString, str(creditsJson["cast"]), str(creditsJson["crew"]), creditsJson["id"])
            # print("credits")
            cursor.execute(insertString, str(jsonObj2['adult']), str(jsonObj2['belongs_to_collection']), jsonObj2['budget'], str(jsonObj2['genres']), str(jsonObj2['homepage']), jsonObj2['id'], str(jsonObj2['imdb_id']), str(jsonObj2['original_language']), str(jsonObj2['original_title']), str(jsonObj2['overview']), jsonObj2['popularity'], str(jsonObj2['poster_path']), str(jsonObj2['production_companies']), str(jsonObj2['production_countries']), jsonObj2['release_date'], jsonObj2['revenue'], str(jsonObj2['runtime']), str(jsonObj2['spoken_languages']), "Released", str(jsonObj2["tagline"]), str(jsonObj2['title']), str(jsonObj2['video']), jsonObj2['vote_average'], jsonObj2['vote_count'])
            # print("insertString")
            cursor.execute("UPDATE [dbo].[showtimefinder_userselectmovies] SET isMovieRec = ?", 0)
            cxn.commit()
            # print("One") 
        # print("finished")
        counter += 1
    cursor.close()
    cxn.close()
    # end = time.time()
    # diff = end - start
except Exception as err:
    print(err)
    sys.exit(1)