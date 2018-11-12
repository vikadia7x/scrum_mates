from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect , HttpResponse
from django.urls import reverse
from showtimefinder.forms import SignUpForm, LoginForm, EditProfileForm
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
from showtimefinder.models import UserProfile, MovieGenreList, MovieGenreSelection, UserSelectMovies
from showtimefinder.models import User
from django.db.models import Q
from bs4 import BeautifulSoup
from django.http import HttpRequest
from requests import get
import geocoder
import requests
from django.core import serializers
import config

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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
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

def select(request):
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
            History = form.cleaned_data.get('History')
            if (History==1):
                genre_list['History'] = History
            else:
                genre_list['History'] = 0
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

        listmovie_History = MovieGenreSelection.objects.filter(History = None).values()
        if(History==1):
            listmovie_History = MovieGenreSelection.objects.filter(History = genre_list['History']).values()
        
        listmovie_Horror = MovieGenreSelection.objects.filter(Horror = None).values()
        if(Horror==1):
            listmovie_History = MovieGenreSelection.objects.filter(Horror = genre_list['Horror']).values()

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
        | listmovie_History
        | listmovie_Horror
        | listmovie_Music
        | listmovie_Mystery
        | listmovie_Romance
        | listmovie_Science
        | listmovie_TV
        | listmovie_Thriller
        | listmovie_Western
        | listmovie_War
        ).distinct().order_by('popularity').reverse()

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
        for movies in userselectmovieslist:
            uSelect = UserSelectMovies(userId=request.user,movieId = movies)
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
        url = 'https://www.imdb.com/showtimes/US/{}'
        response = get(url.format(text))
        movielist = scrapeData(response)

        args = {
            'text': text,
            'form': form,
            'movielist' : movielist
        }
        return render(request, 'landing.html', args)
    else:
        form = SearchForm()
        g = geocoder.ip('me')
        url = 'https://www.imdb.com/showtimes/US/{}'
        response = get(url.format(g.postal))
        movielist = scrapeData(response)
        args = {
            'movielist' : movielist,
            'form': form
        }
        return render(request, 'landing.html', args)

def userprofile(request):
    user = User.objects.filter(username=request.user).values()
    userprofile = UserProfile.objects.filter(user_id = user[0].get('id')).values()
    zipcode = userprofile[0].get('zipcode')
    dob = userprofile[0].get('dateofbirth')
    userdetails = {
    'zipcode': zipcode,
    'dateofbirth': dob}
    return render(request,'userprofile.html', userdetails)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Your details are Updated'
            message = render_to_string('UserEdit_email.html')
            send_mail(subject, message,config.AZURE_SEND_GRID,[user.email])
            return redirect(reverse('userprofile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)

def AboutUs(request):
    return render(request,'AboutUs.html')

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
        return render(request, 'home.html', args)
    else:
        form = SearchForm()
        user = User.objects.filter(username=request.user).values()
        userprofile = UserProfile.objects.filter(user_id = user[0].get('id')).values()
        zipcode = userprofile[0].get('zipcode')
        url = 'https://www.imdb.com/showtimes/US/{}'
        response = get(url.format(zipcode))
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
                    movie_showdate = 'NA'
                movie_details = [
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
                    movie_showdate = 'NA'
                movie_details = [
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
            return movielist