'''
author: Subhradeep Biswas
The following code scrape the imdb site to get the showtime of movies for a user's zipcode and send the user the movie notification
'''

# -*- coding: utf-8 -*-
import csv  # to create a csv file
import requests  # to get info from api
import sys  # for exit
import time  # to prevent exceeding api limit
# import pymssql
import pyodbc
import pandas as pd  # to import dataframe on to a database
# import urllib #to pass through exact pyodbc strin
# from sqlalchemy import create_engine # to get the python sql file on the
import config as cf
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from bs4 import BeautifulSoup
from requests import get


# from django.core.management import setup_environ
# from movieshowtimefinder import settings

# from .tokens import account_activation_token


def scrapeData(response):
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movielist = []
    odditems = html_soup.find_all('div', class_='list_item odd')
    movielistodd = []
    for item in odditems:
        threater_name = item.find('div', class_='fav_box').a.text
        threater_streetaddress = item.find('div', class_='address').find('span',
                                                                         attrs={'itemprop': 'streetAddress'}).text
        threater_addressLocality = item.find('div', class_='address').find('span',
                                                                           attrs={'itemprop': 'addressLocality'}).text
        threater_addressRegion = item.find('div', class_='address').find('span',
                                                                         attrs={'itemprop': 'addressRegion'}).text
        threater_postalCode = item.find('div', class_='address').find('span', attrs={'itemprop': 'postalCode'}).text
        if (item.find('div', class_='address').find('span', attrs={'itemprop': 'telephone'}) is not None):
            threater_telephone = item.find('div', class_='address').find('span', attrs={'itemprop': 'telephone'}).text
        else:
            threater_telephone = 'NA'
        threatre_address = threater_streetaddress + ", " + threater_addressLocality + " " + threater_addressRegion + " " + threater_postalCode
        movies = item.find_all('div', class_='list_item')
        movielistall = []
        movielistall.append(threater_name)
        movielistall.append(threatre_address)
        movielistall.append(threater_telephone)
        for x in movies:
            if ((x.find('div', class_='info').h4.span) is not None):
                movie_name = x.find('div', class_='info').h4.span.a.text
            else:
                movie_name = 'NA'
            if ((x.find('div', class_='image_sm').a) is not None):
                movie_imgURL = x.find('div', class_='image_sm').a.img['src']
            else:
                movie_imgURL = 'NA'
            if (x.find('div', class_='info').time is not None):
                movie_duration = x.find('div', class_='info').time.text
            else:
                movie_duration = 'NA'
            if ((x.find('div', class_='info').strong) is not None):
                movie_rating = x.find('div', class_='info').strong.text
            else:
                movie_rating = 'NA'
            showtime = x.find('div', class_='showtimes')
            if (showtime.find('a', class_='btn2 btn2_simple medium') is not None):
                movie_showtime = showtime.find('a', class_='btn2 btn2_simple medium')['data-displaytimes']
            else:
                movie_showtime = 'NA'
            if (showtime.find('a', class_='btn2 btn2_simple medium') is not None):
                movie_showdate = showtime.find('a', class_='btn2 btn2_simple medium')['data-date']
            else:
                movie_showdate = 'NA'
            movie_details = [
                threater_name,
                movie_name,
                movie_imgURL,
                movie_duration,
                movie_rating,
                movie_showtime,
                movie_showdate
            ]
            movielistall.append(movie_details)
        movielistodd.append(movielistall)
        movielist.append(movielistodd)

    evenitems = html_soup.find_all('div', class_='list_item even')
    movielisteven = []
    for item in evenitems:
        threater_name = item.find('div', class_='fav_box').a.text
        threater_streetaddress = item.find('div', class_='address').find('span',
                                                                         attrs={'itemprop': 'streetAddress'}).text
        threater_addressLocality = item.find('div', class_='address').find('span',
                                                                           attrs={'itemprop': 'addressLocality'}).text
        threater_addressRegion = item.find('div', class_='address').find('span',
                                                                         attrs={'itemprop': 'addressRegion'}).text
        threater_postalCode = item.find('div', class_='address').find('span', attrs={'itemprop': 'postalCode'}).text
        threater_telephone = item.find('div', class_='address').find('span', attrs={'itemprop': 'telephone'}).text
        threatre_address = threater_streetaddress + ", " + threater_addressLocality + " " + threater_addressRegion + " " + threater_postalCode
        movies = item.find_all('div', class_='list_item')
        movielistall = []
        movielistall.append(threater_name)
        movielistall.append(threatre_address)
        movielistall.append(threater_telephone)
        for x in movies:
            if ((x.find('div', class_='info').h4.span) is not None):
                movie_name = x.find('div', class_='info').h4.span.a.text
            else:
                movie_name = 'NA'
            if ((x.find('div', class_='image_sm').a) is not None):
                movie_imgURL = x.find('div', class_='image_sm').a.img['src']
            else:
                movie_imgURL = 'NA'
            if (x.find('div', class_='info').time is not None):
                movie_duration = x.find('div', class_='info').time.text
            else:
                movie_duration = 'NA'
            if ((x.find('div', class_='info').strong) is not None):
                movie_rating = x.find('div', class_='info').strong.text
            else:
                movie_rating = 'NA'
            showtime = x.find('div', class_='showtimes')
            if (showtime.find('a', class_='btn2 btn2_simple medium') is not None):
                movie_showtime = showtime.find('a', class_='btn2 btn2_simple medium')['data-displaytimes']
            else:
                movie_showtime = 'NA'
            if (showtime.find('a', class_='btn2 btn2_simple medium') is not None):
                movie_showdate = showtime.find('a', class_='btn2 btn2_simple medium')['data-date']
            else:
                movie_showdate = 'NA'
            movie_details = [
                threater_name,
                movie_name,
                movie_imgURL,
                movie_duration,
                movie_rating,
                movie_showtime,
                movie_showdate
            ]
            movielistall.append(movie_details)
        movielisteven.append(movielistall)
        movielist.append(movielisteven)
        return movielistall


def sendtoDB(host, uid, pwd, db):
    try:

        cxn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + host + ';DATABASE=' + dbname + ';UID=' + uid + ';PWD=' + pwd)

        # -- Begin: Added by Subhradeep -- #
        li = []
        print("Begin")

        df_zip = pd.read_sql_query(
            'select user_id, zipcode from dbo.showtimefinder_userprofile a   where email_confirmed = 1',
            con=cxn)
        moviecursor = cxn.cursor()
        moviecursor.execute('Truncate table user_notification_details;')
        movieinsert = "INSERT INTO user_notification_details(user_id, movie_name, showdate, showtime, cinema) values(?, ?, ?, ?, ?);"
        for index, row in df_zip.iterrows():
            zipcode = (row['zipcode'])
            url = 'https://www.imdb.com/showtimes/US/{}'
            response = get(url.format(zipcode))
            li = scrapeData(response)
            for i in range(0, len(li)):
                moviecursor.execute(movieinsert, str(row['user_id']), str(li[i][1]), str(li[i][-1]), str(li[i][-2]),
                                    str(li[i][0]))
                moviecursor.commit()

        # print(li[1])
        # print(li[1][1])

        # settings.configure()
        df_send = pd.read_sql_query(
            'select a.Original_title title, a.imdb_id imdb_id, a.poster_path poster_path, a.popularity popularity, c.email email from NowPlayingData_tmp a, user_notification b, auth_user c where b.movie_id = a.id and b.user_id = c.id',
            con=cxn)
        cxn.close()
        subject = 'Movie notification'
        print(subject)
        print(df_send)

        for index, row in df_send.iterrows():
            message = "Movie Name: " + row['title'] + "\n"
            "Popularity: " + str(row['popularity']) + "\n"

            # message = render_to_string('UserNotifyEmail.html')

            # from_email = settings.EMAIL_HOST_USER
            # to_email = [from_email , row['email']]
            send_mail(subject, message, cf.AZURE_SEND_GRID, [row['email']])
        # -- End: Added by Subhradeep -- #

    except Exception as err:
        print("SendtoDB")
        print(err)
        # sys.exit(1)

    returnStr = "Everything printed well"
    return returnStr


try:


    api_key = cf.TMDB_API_KEY
    server = cf.DATABASE_HOST_SERVER
    dbname = cf.DATABASE_NAME
    user = cf.DATABASE_USER
    password = cf.DATABASE_PASSWORD


    print(sendtoDB(server, user, password, dbname))


except requests.exceptions.HTTPError as err:
    print("Main method")
    print(err)
    sys.exit(1)
