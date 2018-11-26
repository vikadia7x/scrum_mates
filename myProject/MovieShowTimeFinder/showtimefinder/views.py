from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect , HttpResponse
from django.urls import reverse
from showtimefinder.forms import SignUpForm, LoginForm, EditProfileForm, EditUserProfileForm
from showtimefinder.forms import SearchForm, MovieSelection
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from showtimefinder.models import UserProfile, MovieGenreList, MovieGenreSelection, UserSelectMovies,RecommendedMovie
from showtimefinder.models import User
from django.db.models import Q
from bs4 import BeautifulSoup
from django.http import HttpRequest
from requests import get
import geocoder
import requests
from django.core import serializers
import config, pyodbc, datetime, ast, math, os
import threading
import multiprocessing
import threading, queue
from operator import itemgetter


def createDBConnection():
    server = config.DATABASE_HOST_SERVER
    print(server)
    database = config.DATABASE_NAME
    username = config.DATABASE_USER
    password = config.DATABASE_PASSWORD
    #driver='/usr/local/lib/libmsodbcsql.13.dylib'
    # driver = {ODBC Driver 13 for SQL Server}
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user.userprofile.dateofbirth = form.cleaned_data.get('dateofbirth')
            user.userprofile.zipcode = form.cleaned_data.get('zipcode')
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message,config.AZURE_SEND_GRID,[user.email])
        return redirect('landing.html')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Account activated successfully')
    else:
        return HttpResponse('Activation link is invalid!')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                userp = UserProfile.objects.filter(user_id = user.id).values()
                isFirstLogin = userp[0].get('isFirstLogin')
                if(isFirstLogin):
                    user.userprofile.isFirstLogin = 0
                    user.save()
                    return redirect('select.html')
                else:
                    return redirect('home.html')
            else:
                messages.error(request,'Username or Password is incorrect. Please try again!')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             zipcode = form.cleaned_data.get('zipcode')
#             dateofbirth = form.cleaned_data.get('dateofbirth')
#             user = User.objects.filter(username=request.user).values()
#             UserProfile.objects.filter(user_id = user[0].get('id')).update(zipcode = zipcode,dateofbirth=dateofbirth)

#         return redirect('userprofile.html')
#     else:
#         form = EditProfileForm(instance=request.user.userprofile)
#         args = {'form': form}
#         return render(request, 'edit_profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form1 = EditProfileForm(request.POST,instance = request.user)
        form2 = EditUserProfileForm(request.POST,instance = request.user.userprofile)
        if form1.is_valid():
            if(form1.cleaned_data.get('first_name') is not None):
                firstname = form1.cleaned_data.get('first_name')
                print(firstname)
            else:
                user = User.objects.filter(username=request.user).values()
                firstname = user[0].get('first_name')

            if(form1.cleaned_data.get('last_name') is not None):
                lastname = form1.cleaned_data.get('last_name')
            else:
                user = User.objects.filter(username=request.user).values()
                lastname = user[0].get('last_name')

            if(form1.cleaned_data.get('email') is not None):
                email = form1.cleaned_data.get('email')
            else:
                user = User.objects.filter(username=request.user).values()
                email = user[0].get('email')
            User.objects.filter(username=request.user).update(first_name = firstname, last_name = lastname, email = email)
        if form2.is_valid():
            zipcode = form2.cleaned_data.get('zipcode')
            print(zipcode)
            dateofbirth = form2.cleaned_data.get('dateofbirth')
            user = User.objects.filter(username=request.user).values()
            UserProfile.objects.filter(user_id = user[0].get('id')).update(zipcode = zipcode,dateofbirth=dateofbirth)
            print(UserProfile.objects.filter(user_id = user[0].get('id')))
        return redirect('userprofile.html')

    else:
        form1 = EditProfileForm(instance = request.user)
        form2 = EditUserProfileForm(instance = request.user.userprofile)
        args = {'form1': form1, 'form2': form2}
        return render(request, 'edit_profile.html', args)

def userprofile(request):
    user = User.objects.filter(username=request.user).values()
    userprofile = UserProfile.objects.filter(user_id = user[0].get('id')).values()
    zipcode = userprofile[0].get('zipcode')
    dob = userprofile[0].get('dateofbirth')
    userdetails = {
    'zipcode': zipcode,
    'dateofbirth': dob}
    return render(request,'userprofile.html', userdetails)

def select(request):
    user = User.objects.filter(username=request.user).values()
    #userprofile = UserProfile.objects.filter(user_id = user[0].get('id')).values()
    UserSelectMovies.objects.filter(userId = user[0].get('id')).update(isMovieRec = 0)
    if request.method == 'POST':
        form = MovieSelection(request.POST)
        if form.is_valid():
            genre_list ={}
            Action = form.cleaned_data.get('Action')
            if (Action==1):
                genre_list['Action'] = Action
            else:
                genre_list['Action'] = 0
            Adventure = form.cleaned_data.get('Adventure')
            if (Adventure==1):
                genre_list['Adventure'] = Adventure
            else:
                genre_list['Adventure'] = 0
            Animation = form.cleaned_data.get('Animation')
            if (Animation==1):
                genre_list['Animation'] = Animation
            else:
                genre_list['Animation'] = 0
            Comedy = form.cleaned_data.get('Comedy')
            if (Comedy==1):
                genre_list['Comedy'] = Comedy
            else:
                genre_list['Comedy'] = 0
            Crime = form.cleaned_data.get('Crime')
            if (Crime==1):
                genre_list['Crime'] = Crime
            else:
                genre_list['Crime'] = 0
            Documentary = form.cleaned_data.get('Documentary')
            if (Documentary==1):
                genre_list['Documentary'] = Documentary
            else:
                genre_list['Documentary'] = 0
            Drama = form.cleaned_data.get('Drama')
            if (Drama==1):
                genre_list['Drama'] = Drama
            else:
                genre_list['Drama'] = 0
            Family = form.cleaned_data.get('Family')
            if (Family==1):
                genre_list['Family'] = Family
            else:
                genre_list['Family'] = 0
            Fantasy = form.cleaned_data.get('Fantasy')
            if (Fantasy==1):
                genre_list['Fantasy'] = Fantasy
            else:
                genre_list['Fantasy'] = 0
            Horror = form.cleaned_data.get('Horror')
            if (Horror==1):
                genre_list['Horror'] = Horror
            else:
                genre_list['Horror'] = 0
            Music = form.cleaned_data.get('Music')
            if (Music==1):
                genre_list['Music'] = Music
            else:
                genre_list['Music'] = 0
            Mystery = form.cleaned_data.get('Mystery')
            if (Mystery==1):
                genre_list['Mystery'] = Mystery
            else:
                genre_list['Mystery'] = 0
            Romance = form.cleaned_data.get('Romance')
            if (Romance==1):
                genre_list['Romance'] = Romance
            else:
                genre_list['Romance'] = 0
            Science = form.cleaned_data.get('Science')
            if (Science==1):
                genre_list['Science'] = Science
            else:
                genre_list['Science'] = 0
            TV = form.cleaned_data.get('TV')
            if (TV==1):
                genre_list['TV'] = TV
            else:
                genre_list['TV'] = 0
            Thriller = form.cleaned_data.get('Thriller')
            if (Thriller==1):
                genre_list['Thriller'] = Thriller
            else:
                genre_list['Thriller'] = 0
            War = form.cleaned_data.get('War')
            if (War==1):
                genre_list['War'] = War
            else:
                genre_list['War'] = 0
            Western = form.cleaned_data.get('Western')
            if (Western==1):
                genre_list['Western'] = Western
            else:
                genre_list['Western'] = 0

        listmovie_Action = MovieGenreSelection.objects.filter(Action = None).values()
        if(Action==1):
            listmovie_Action = MovieGenreSelection.objects.filter(Action = genre_list['Action']).values()

        listmovie_Adventure = MovieGenreSelection.objects.filter(Adventure = None).values()
        if(Adventure==1):
            listmovie_Adventure = MovieGenreSelection.objects.filter(Adventure = genre_list['Adventure']).values()

        listmovie_Animation = MovieGenreSelection.objects.filter(Animation = None).values()
        if(Animation==1):
            listmovie_Animation = MovieGenreSelection.objects.filter(Animation = genre_list['Animation']).values()

        listmovie_Comedy = MovieGenreSelection.objects.filter(Comedy = None).values()
        if(Comedy==1):
            listmovie_Comedy = MovieGenreSelection.objects.filter(Comedy = genre_list['Comedy']).values()

        listmovie_Crime = MovieGenreSelection.objects.filter(Crime = None).values()
        if(Crime==1):
            listmovie_Crime = MovieGenreSelection.objects.filter(Crime = genre_list['Crime']).values()

        listmovie_Documentary = MovieGenreSelection.objects.filter(Documentary = None).values()
        if(Documentary==1):
            listmovie_Documentary = MovieGenreSelection.objects.filter(Documentary = genre_list['Documentary']).values()

        listmovie_Drama = MovieGenreSelection.objects.filter(Drama = None).values()
        if(Drama==1):
            listmovie_Drama = MovieGenreSelection.objects.filter(Drama = genre_list['Drama']).values()

        listmovie_Fantasy = MovieGenreSelection.objects.filter(Fantasy = None).values()
        if(Fantasy==1):
            listmovie_Fantasy = MovieGenreSelection.objects.filter(Fantasy = genre_list['Fantasy']).values()

        listmovie_Family = MovieGenreSelection.objects.filter(Family = None).values()
        if(Family==1):
            listmovie_Family = MovieGenreSelection.objects.filter(Family = genre_list['Family']).values()

        listmovie_Horror = MovieGenreSelection.objects.filter(Horror = None).values()
        if(Horror==1):
            listmovie_Horror = MovieGenreSelection.objects.filter(Horror = genre_list['Horror']).values()

        listmovie_Music = MovieGenreSelection.objects.filter(Music = None).values()
        if(Music==1):
            listmovie_Music = MovieGenreSelection.objects.filter(Music = genre_list['Music']).values()

        listmovie_Mystery = MovieGenreSelection.objects.filter(Mystery = None).values()
        if(Mystery==1):
            listmovie_Mystery = MovieGenreSelection.objects.filter(Mystery = genre_list['Mystery']).values()

        listmovie_Romance = MovieGenreSelection.objects.filter(Romance = None).values()
        if(Romance==1):
            listmovie_Romance = MovieGenreSelection.objects.filter(Romance = genre_list['Romance']).values()

        listmovie_Science = MovieGenreSelection.objects.filter(Science = None).values()
        if(Science==1):
            listmovie_Science = MovieGenreSelection.objects.filter(Science = genre_list['Science']).values()

        listmovie_TV = MovieGenreSelection.objects.filter(TV = None).values()
        if(TV==1):
            listmovie_TV = MovieGenreSelection.objects.filter(TV = genre_list['TV']).values()

        listmovie_Thriller = MovieGenreSelection.objects.filter(Thriller = None).values()
        if(Thriller==1):
            listmovie_Thriller = MovieGenreSelection.objects.filter(Thriller = genre_list['Thriller']).values()

        listmovie_Western = MovieGenreSelection.objects.filter(Western = None).values()
        if(Western==1):
            listmovie_Western = MovieGenreSelection.objects.filter(Western = genre_list['Western']).values()

        listmovie_War = MovieGenreSelection.objects.filter(War = None).values()
        if(War==1):
            listmovie_War = MovieGenreSelection.objects.filter(War = genre_list['War']).values()

        listmovie = (listmovie_Action
        | listmovie_Adventure
        | listmovie_Animation
        | listmovie_Comedy
        | listmovie_Crime
        | listmovie_Drama
        | listmovie_Documentary
        | listmovie_Family
        | listmovie_Fantasy
        | listmovie_Horror
        | listmovie_Music
        | listmovie_Mystery
        | listmovie_Romance
        | listmovie_Science
        | listmovie_TV
        | listmovie_Thriller
        | listmovie_Western
        | listmovie_War
        ).distinct().filter(votecount__gte='100').order_by('voteavg','popularity').reverse()

        list_genre = list(listmovie)
        list_genre = list_genre[:20]

        request.session['list_genre'] = list_genre
        return redirect('displaymovies.html')
    else:
        form = MovieSelection()
        return render(request, 'select.html', {'form':form})

def displaymovies(request):
    if request.method == 'POST':
        userselectmovieslist = request.POST.getlist("check")
        print(userselectmovieslist)
        for movies in userselectmovieslist:
            movieselect = MovieGenreSelection.objects.filter(tmdbId=movies).values()
            uSelect = UserSelectMovies(userId=request.user,tmdbId = movies, movieName = movieselect[0].get('title'))
            uSelect.save()
        return redirect('home.html')
    else:
        list_genre = request.session.get('list_genre')
        return render(request, 'displaymovies.html',{'list_genre':list_genre})


def landing(request):
    if(request.method == 'POST'):
        form  = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            form = SearchForm()

        #call for imdbid in a list
        url = 'https://www.imdb.com/showtimes/location/US/{}'
        response = get(url.format(text))
        getmovielist = scrapeMovie(response, text)

        #call for getting threatre list by passing movielist
        movieThreatreList = scrapeThreatre(getmovielist,text)

        #get movie data from db to display
        movie_info_list = getMovieInfoFromDB(set(getmovielist))

        #popular movie posters in HD
        pickpopularmovies = 'https://www.imdb.com/showtimes/location/US/{}'
        pickpopularmoviesresp = get(pickpopularmovies.format(text))
        popularmovieposterlinks = scrapePosterInfoData(pickpopularmoviesresp)

        #latest movie posters in HD
        picklatestmovies = 'https://www.imdb.com/showtimes/location/US/{}?sort=release_date,desc&st_dt='+str(datetime.datetime.now().strftime("%Y-%m-%d"))+'&mode=showtimes_grid&page=1'
        picklatestmoviesrep = get(picklatestmovies.format(text))
        picklatestmoviesreplinks = scrapePosterInfoData(picklatestmoviesrep)

        args = {
            'movie_info_list' : movie_info_list,
            'movieThreatreList' : movieThreatreList,
            'form': form,
            'popular_movies' : popularmovieposterlinks,
            'latest_movies' : picklatestmoviesreplinks
        }
        return render(request, 'landing.html', args)
    else:
        form = SearchForm()
        g = geocoder.ip('me')
        if (g.postal is not '85281'):
            text = '85281'
        else:
            text = g.postal

        #call for imdbid in a list
        url = 'https://www.imdb.com/showtimes/location/US/{}'
        response = get(url.format(text))

        getmovielist = scrapeMovie(response, text)

        #call for getting threatre list by passing movielist
        movieThreatreList = scrapeThreatre(getmovielist,text)

        #get movie data from db to display
        movie_info_list = getMovieInfoFromDB(set(getmovielist))

        #popular movie posters in HD
        pickpopularmovies = 'https://www.imdb.com/showtimes/location/US/{}'
        pickpopularmoviesresp = get(pickpopularmovies.format(text))
        popularmovieposterlinks = scrapePosterInfoData(pickpopularmoviesresp)

        #latest movie posters in HD
        picklatestmovies = 'https://www.imdb.com/showtimes/location/US/{}?sort=release_date,desc&st_dt='+str(datetime.datetime.now().strftime("%Y-%m-%d"))+'&mode=showtimes_grid&page=1'
        picklatestmoviesrep = get(picklatestmovies.format(text))
        picklatestmoviesreplinks = scrapePosterInfoData(picklatestmoviesrep)

        args = {
            'movie_info_list' : movie_info_list,
            'movieThreatreList' : movieThreatreList,
            'form': form,
            'popular_movies' : popularmovieposterlinks,
            'latest_movies' : picklatestmoviesreplinks
        }
        return render(request, 'landing.html', args)

def AboutUs(request):
    return render(request,'AboutUs.html')

def home(request):
    os.system("cd ..")
    os.system("python final_recommendation.py")
    os.system("cd showtimefinder")
    if(request.method == 'POST'):
        form  = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            form = SearchForm()

        #call for imdbid in a list
        url = 'https://www.imdb.com/showtimes/location/US/{}'
        response = get(url.format(text))
        getmovielist = scrapeMovie(response, text)

        #call for getting threatre list by passing movielist
        movieThreatreList = scrapeThreatre(getmovielist,text)

        #get movie data from db to display
        movie_info_list = getMovieInfoFromDB(set(getmovielist))

        #popular movie posters in HD
        pickpopularmovies = 'https://www.imdb.com/showtimes/location/US/{}'
        pickpopularmoviesresp = get(pickpopularmovies.format(text))
        popularmovieposterlinks = scrapePosterInfoData(pickpopularmoviesresp)

        #latest movie posters in HD
        picklatestmovies = 'https://www.imdb.com/showtimes/location/US/{}?sort=release_date,desc&st_dt='+str(datetime.datetime.now().strftime("%Y-%m-%d"))+'&mode=showtimes_grid&page=1'
        picklatestmoviesrep = get(picklatestmovies.format(text))
        picklatestmoviesreplinks = scrapePosterInfoData(picklatestmoviesrep)

        args = {
            'movie_info_list' : movie_info_list,
            'movieThreatreList' : movieThreatreList,
            'form': form,
            'popular_movies' : popularmovieposterlinks,
            'latest_movies' : picklatestmoviesreplinks
        }
        return render(request, 'home.html', args)
    else:
        #os.system("python hello.py")
        form = SearchForm()
        user = User.objects.filter(username=request.user).values()
        userprofile = UserProfile.objects.filter(user_id = user[0].get('id')).values()
        zipcode = userprofile[0].get('zipcode')
        text = zipcode
        uSelect = RecommendedMovie.objects.filter(userId = request.user).values()
        getmovielist = []
        i = 0
        while (i!=len(uSelect)):
            getmovielist.append(uSelect[i].get('imdb_id'))
            i = i+1

        #movie theatre list
        movieThreatreList = scrapeThreatre(set(getmovielist),text)
        #get movie data from db to display
        movie_info_list = getMovieInfoFromDB(set(getmovielist))

        res= sorted(movie_info_list, key=itemgetter('popularity'),reverse=True)
        # res2= sorted(res1, key=itemgetter('popularity'),reverse=True)

        #print(res)

        args = {
            'movie_info_list' : res,
            'movieThreatreList' : movieThreatreList,
            'form': form
        }
        return render(request, 'home.html', args)


def scrapeMovie(response,text):
    movie_list = []
    html_soup= BeautifulSoup(response.text, 'html.parser')
    soupdata = html_soup.find_all('div', class_ = 'lister-item-image ribbonize')
    for item in soupdata[:5]:
        imdbId = item['data-tconst']
        movie_list.append(imdbId)
    return movie_list

def scrapeThreatre(movielist, text):
    movie_threatre = []
    url = 'https://www.imdb.com/showtimes/title/{0}/US/{1}'
    for imdbid in movielist:
        response = get(url.format(imdbid,text))
        html_soup_1= BeautifulSoup(response.text, 'html.parser')
        soupdata = html_soup_1.find_all('div', class_ = 'list_item odd')
        for item in soupdata[:1]:
            threater_name = item.find('div', class_= 'fav_box').a.text
            threater_streetaddress = item.find('div', class_='address').find('span', attrs = {'itemprop':'streetAddress'}).text
            threater_addressLocality = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressLocality'}).text
            threater_addressRegion = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressRegion'}).text
            threater_postalCode = item.find('div', class_='address').find('span', attrs = {'itemprop':'postalCode'}).text
            threater_telephone = item.find('div', class_='address').find('span', attrs = {'itemprop':'telephone'}).text
            if(item.find('a', class_ = 'btn2 btn2_simple medium') is None):
                movie_showdate = 'NA'
            else:
                movie_showdate = item.find('a', class_ = 'btn2 btn2_simple medium')['data-date']
            if(item.find('a', class_ = 'btn2 btn2_simple medium') is None):
                movie_showtime = 'NA'
            else:
                movie_showtime = item.find('a', class_ = 'btn2 btn2_simple medium')['data-displaytimes']
            movie_info = {
                'imdbid': imdbid,
                'threater_name' : threater_name,
                'threater_streetaddress' : threater_streetaddress,
                'threater_addressLocality' : threater_addressLocality,
                'threater_addressRegion' : threater_addressRegion,
                'threater_postalCode' : threater_postalCode,
                'threater_telephone' : threater_telephone,
                'movie_showdate': movie_showdate,
                'movie_showtime': movie_showtime
                }
            movie_threatre.append(movie_info)

    for imdbid in movielist:
        response = get(url.format(imdbid,text))
        html_soup_1= BeautifulSoup(response.text, 'html.parser')
        soupdata = html_soup_1.find_all('div', class_ = 'list_item even')
        for item in soupdata[:1]:
            threater_name = item.find('div', class_= 'fav_box').a.text
            threater_streetaddress = item.find('div', class_='address').find('span', attrs = {'itemprop':'streetAddress'}).text
            threater_addressLocality = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressLocality'}).text
            threater_addressRegion = item.find('div', class_='address').find('span', attrs = {'itemprop':'addressRegion'}).text
            threater_postalCode = item.find('div', class_='address').find('span', attrs = {'itemprop':'postalCode'}).text
            threater_telephone = item.find('div', class_='address').find('span', attrs = {'itemprop':'telephone'}).text
            if(item.find('a', class_ = 'btn2 btn2_simple medium') is None):
                movie_showdate = 'NA'
            else:
                movie_showdate = item.find('a', class_ = 'btn2 btn2_simple medium')['data-date']
            if(item.find('a', class_ = 'btn2 btn2_simple medium') is None):
                movie_showdate = 'NA'
            else:
                movie_showtime = item.find('a', class_ = 'btn2 btn2_simple medium')['data-displaytimes']

            movie_info = {
                'imdbid': imdbid,
                'threater_name' : threater_name,
                'threater_streetaddress' : threater_streetaddress,
                'threater_addressLocality' : threater_addressLocality,
                'threater_addressRegion' : threater_addressRegion,
                'threater_postalCode' : threater_postalCode,
                'threater_telephone' : threater_telephone,
                'movie_showdate': movie_showdate,
                'movie_showtime': movie_showtime
                }
            movie_threatre.append(movie_info)
    return movie_threatre

def scrapePosterInfoData(pickpopularmoviesresp):
    cnxn = createDBConnection()
    cursor = cnxn.cursor()
    html_soup = BeautifulSoup(pickpopularmoviesresp.text, 'html.parser')
    poster_link = []
    poster = html_soup.find_all('h3', class_ = 'lister-item-header')
    for item in poster[:30]:
        movieid = item.find('a')
        imdbid = movieid['href'].split('/')[3]
        query_meta = "SELECT poster_path FROM [dbo].[NowPlayingData] Where imdb_id='" + imdbid +"'"
        cursor.execute(query_meta)
        result = cursor.fetchall()
        for row in result :
            if(row[0] is not None):
                poster_link.append("https://image.tmdb.org/t/p/original/"+row[0])
    return poster_link

def getMovieInfoFromDB(imdbList):
    cnxn = createDBConnection()
    cursor = cnxn.cursor()
    movie_info_list = []
    for item in imdbList:
        query_meta = "SELECT title, convert(float,popularity) as p, overview, release_date,runtime,vote_average,poster_path,imdb_id FROM [dbo].[NowPlayingData] Where imdb_id='" + item +"'"
        cursor.execute(query_meta)
        result = cursor.fetchall()
        for row in result :
            movie_info = {
                'title': row[0],
                'popularity':row[1],
                'overview': row[2],
                'release_date': datetime.datetime.strftime(row[3],'%b. %d %Y'),
                'runtime': row[4],
                'vote_average': int(math.floor(float(row[5]))/2),
                'poster': "https://image.tmdb.org/t/p/w500" + row[6],
                'poster_path' : "https://image.tmdb.org/t/p/original/"+row[6],
                'imdbId': row[7]
            }
            movie_info_list.append(movie_info)
    return movie_info_list

def movieInfo(request):
   query = request.GET.get('id')
   api_key = config.TMDB_API_KEY
   # connect to the ODBC database
   cxn = createDBConnection()
   cursor = cxn.cursor()
    
   infoString = "SELECT budget, genres, homepage, original_title, overview, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, tagline, title FROM [dbo].[NowPlayingData] WHERE imdb_id='"+ query +"'"
   cursor.execute(infoString)
   result1 = cursor.fetchall()
   movieIdString = "SELECT movieId, tmdbId FROM [dbo].[NowPlayingLinks] WHERE imdbId='"+query+"'"
   cursor.execute(movieIdString)
   result2 = cursor.fetchall()
   castString = "SELECT cast, crew FROM [dbo].[NowPlayingCredits] WHERE id='"+str(result2[0][1])+"'" #tmdbId
   cursor.execute(castString)
   result3 = cursor.fetchall()
   
   #get the poster path image
   posterlink = "https://image.tmdb.org/t/p/original/"+result1[0][5]

   #Get video info:
   video = requests.get("https://api.themoviedb.org/3/movie/"+query+"/videos?api_key="+api_key+"&language=en-US").json()
   videoLink= "https://www.youtube.com/embed/"
   videoLink = videoLink+str(video["results"][0]["key"])
  

   # convert genres to a list
   genre = []
   lang = []
   company =[]
   countries=[]
   # Split string values
   langList =result1[0][11].split()
   genreList= result1[0][1].split()
   companyList = result1[0][6].split(",")
   countryList = result1[0][7].split()
   for i in range(len(genreList)):
       if(genreList[i] == "'name':"):
           genre.append(genreList[i+1][1:-3]) # remove unnecessary elements
    
   for i in range(len(langList)):
        if(langList[i]=="'name':"):
            lang.append(langList[i+1][1:-3])
   
   for i in range(len(companyList)):
       if("'name':" in companyList[i]):
            company.append(companyList[i][10:-1])
    
   for i in range(len(countryList)):
        if(countryList[i] == "'name':"):
            countries.append(countryList[i-1][1:-2])
      
   context = {
       'budget' : result1[0][0],
       'genres' : genre,
       'homepage' : result1[0][2],
       'originalTitle' : result1[0][3],
       'overview': result1[0][4],
       'productionCompanies': company,
       'productionCountries' : countries,
       'releaseDate' : result1[0][8],
       'revenue' : result1[0][9],
       'runtime' : result1[0][10],
       'spokenLanguages' : lang,
       'tagline' : result1[0][12],
       'title' : result1[0][13],
       'movieId' : result2[0][0],
       'movieCast' : result3[0][0],
       'movieCrew' : result3[0][1],
       'posterPath' : posterlink,
       'video' : videoLink
   } 
   return render(request,'movie_info.html', context)
