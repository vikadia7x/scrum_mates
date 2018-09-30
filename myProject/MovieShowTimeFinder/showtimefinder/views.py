from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from showtimefinder.forms import SignUpForm
from showtimefinder.forms import SearchForm
from showtimefinder.models import User
from showtimefinder.models import User
from bs4 import BeautifulSoup
from django.http import HttpRequest
from requests import get
import re
import geocoder
import socket

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        obj = User()
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            obj.first_name = form.cleaned_data['first_name']
            obj.last_name = form.cleaned_data['last_name']
            obj.email = form.cleaned_data['email']
            obj.dateofbirth = form.cleaned_data['dateofbirth']
            obj.save()
            #login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def landing(request):
    return render(request,'landing.html')

def userprofile(request):
    #print("Hi ! Welcome")
    args = {'user': request.user}
    return render(request,'userprofile.html', args)

# def home(request):
#     return render(request,'home.html')

def home(request):
    if(request.method == 'POST'):
        form  = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            form = SearchForm()
        url = 'https://www.imdb.com/showtimes/US/{}'
        response = get(url.format(text))
        movielist = scrapeData(response)

        args = {
            'text': text,
            'form': form,
            'movielist' : movielist
        }
        #print(args['movielist'][0][0])
        return render(request, 'home.html', args)
    else:
        #print("here")
        form = SearchForm()
        g = geocoder.ip('me')
        print(g)
        url = 'https://www.imdb.com/showtimes/US/{}'
        response = get(url.format(g.postal))
        #text = '85281'
        #response = get(url.format(text))
        movielist = scrapeData(response)
        args = {
            'movielist' : movielist,
            'form': form
        }
        return render(request, 'home.html', args)

def scrapeData(response):
        html_soup = BeautifulSoup(response.text, 'html.parser')
        movielist = []
        odditems = html_soup.find_all('div', class_ = 'list_item odd')
        movielistodd = []
        for item in odditems:
            threater_name = item.find('div', class_= 'fav_box').a.text
            threater_streetaddress = item.find('div', class_='address').find('span', attrs = {'itemprop':'streetAddress'}).text
            threater_addressLocality = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressLocality'}).text
            threater_addressRegion = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressRegion'}).text
            threater_postalCode = item.find('div', class_='address').find('span', attrs = {'itemprop':'postalCode'}).text
            if(item.find('div', class_='address').find('span', attrs = {'itemprop':'telephone'}) is not None):
                threater_telephone = item.find('div', class_='address').find('span', attrs = {'itemprop':'telephone'}).text
            else:
                threater_telephone = 'NA'
            threatre_address = threater_streetaddress + ", " + threater_addressLocality + " " + threater_addressRegion + " " + threater_postalCode
            movies = item.find_all('div', class_ = 'list_item')
            movielistall = []
            movielistall.append(threater_name)
            movielistall.append(threatre_address)
            movielistall.append(threater_telephone)
            for x in movies:
                if((x.find('div', class_ = 'info').h4.span) is not None):
                    movie_name = x.find('div', class_ = 'info').h4.span.a.text
                else:
                    movie_name = 'NA'
                if((x.find('div', class_ = 'image_sm').a) is not None):
                    movie_imgURL = x.find('div', class_ = 'image_sm').a.img['src']
                else:
                    movie_imgURL = 'NA'
                if(x.find('div', class_ = 'info').time is not None):
                    movie_duration = x.find('div', class_ = 'info').time.text
                else:
                    movie_duration = 'NA'
                if((x.find('div', class_ = 'info').strong) is not None):
                    movie_rating = x.find('div', class_ = 'info').strong.text
                else:
                    movie_rating = 'NA'
                showtime = x.find('div' , class_ = 'showtimes')
                if(showtime.find('a', class_ = 'btn2 btn2_simple medium') is not None):
                    movie_showtime = showtime.find('a', class_ = 'btn2 btn2_simple medium')['data-displaytimes']
                else:
                    movie_showtime = 'NA'
                if(showtime.find('a', class_ = 'btn2 btn2_simple medium') is not None):
                    movie_showdate = showtime.find('a', class_ = 'btn2 btn2_simple medium')['data-date']
                else:
                    movie_showtime = 'NA'
                movie_details = {
                    'movie_name' : movie_name,
                    'movie_imgURL' : movie_imgURL,
                    'movie_duration' : movie_duration,
                    'movie_rating' : movie_rating,
                    'movie_showtime' : movie_showtime,
                    'movie_showdate' : movie_showdate
                }
                movielistall.append(dict(movie_details))
            movielistodd.append(movielistall)
            movielist.append(movielistodd)


        evenitems = html_soup.find_all('div', class_ = 'list_item even')
        movielisteven = []
        for item in evenitems:
            threater_name = item.find('div', class_= 'fav_box').a.text
            threater_streetaddress = item.find('div', class_='address').find('span', attrs = {'itemprop':'streetAddress'}).text
            threater_addressLocality = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressLocality'}).text
            threater_addressRegion = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressRegion'}).text
            threater_postalCode = item.find('div', class_='address').find('span', attrs = {'itemprop':'postalCode'}).text
            threater_telephone = item.find('div', class_='address').find('span', attrs = {'itemprop':'telephone'}).text
            threatre_address = threater_streetaddress + ", " + threater_addressLocality + " " + threater_addressRegion + " " + threater_postalCode
            movies = item.find_all('div', class_ = 'list_item')
            movielistall = []
            movielistall.append(threater_name)
            movielistall.append(threatre_address)
            movielistall.append(threater_telephone)
            for x in movies:
                if((x.find('div', class_ = 'info').h4.span) is not None):
                    movie_name = x.find('div', class_ = 'info').h4.span.a.text
                else:
                    movie_name = 'NA'
                if((x.find('div', class_ = 'image_sm').a) is not None):
                    movie_imgURL = x.find('div', class_ = 'image_sm').a.img['src']
                else:
                    movie_imgURL = 'NA'
                if(x.find('div', class_ = 'info').time is not None):
                    movie_duration = x.find('div', class_ = 'info').time.text
                else:
                    movie_duration = 'NA'
                if((x.find('div', class_ = 'info').strong) is not None):
                    movie_rating = x.find('div', class_ = 'info').strong.text
                else:
                    movie_rating = 'NA'
                showtime = x.find('div' , class_ = 'showtimes')
                if(showtime.find('a', class_ = 'btn2 btn2_simple medium') is not None):
                    movie_showtime = showtime.find('a', class_ = 'btn2 btn2_simple medium')['data-displaytimes']
                else:
                    movie_showtime = 'NA'
                if(showtime.find('a', class_ = 'btn2 btn2_simple medium') is not None):
                    movie_showdate = showtime.find('a', class_ = 'btn2 btn2_simple medium')['data-date']
                else:
                    movie_showtime = 'NA'
                movie_details = {
                    'movie_name' : movie_name,
                    'movie_imgURL' : movie_imgURL,
                    'movie_duration' : movie_duration,
                    'movie_rating' : movie_rating,
                    'movie_showtime' : movie_showtime,
                    'movie_showdate' : movie_showdate
                }
                movielistall.append(dict(movie_details))
            movielisteven.append(movielistall)
            movielist.append(movielisteven)
            return movielist