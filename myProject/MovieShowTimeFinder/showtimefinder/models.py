from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='userprofile')
    dateofbirth = models.DateField(blank=False, default = '1992-01-01')
    zipcode = models.TextField(blank=True)
    isFirstLogin = models.BooleanField(default=1)

# class MovieMetaData(models.Model):
#     adult = models.TextField(null=True)
#     belongs_to_collection = models.TextField(null=True)
#     budget = models.TextField(null=True)
#     genres = models.TextField(null=True)
#     homepage = models.TextField(null=True)
#     movie_id = models.TextField(null=True)
#     imdb_id = models.TextField(null=True)
#     original_language = models.TextField(null=True)
#     original_title = models.TextField(null=True)
#     overview = models.TextField(null=True)
#     popularity = models.TextField(null=True)
#     poster_path = models.TextField(null=True)
#     production_companies = models.TextField(null=True)
#     production_countries = models.TextField(null=True)
#     release_date = models.TextField(null=True)
#     revenue = models.TextField(null=True)
#     runtime = models.TextField(null=True)
#     spoken_languages = models.TextField(null=True)
#     status = models.TextField(null=True)
#     tagline = models.TextField(null=True)
#     title = models.TextField(null=True)
#     video = models.TextField(null=True)
#     vote_average = models.TextField(null=True)
#     vote_count = models.TextField(null=True)

# class MovieGenre(models.Model):
#     movieId = models.TextField(null=True)
#     title = models.TextField(null=True)
#     genre = models.TextField(null=True)

class UserSelectMovies(models.Model):
    userId = models.TextField(null=True)
    movieId = models.TextField(null=True)

class MovieGenreList(models.Model):
    genreid = models.TextField(null=True)
    genre = models.TextField(null=True)

class MovieGenreSelection(models.Model):
    movieId = models.TextField(null=True)
    tmdbId = models.TextField(null=True)
    title = models.TextField(null=True)
    Action = models.BooleanField(null=True)
    Adventure = models.BooleanField(null=True)
    Animation = models.BooleanField(null=True)
    Comedy = models.BooleanField(null=True)
    Crime = models.BooleanField(null=True)
    Documentary = models.BooleanField(null=True)
    Drama = models.BooleanField(null=True)
    Family = models.BooleanField(null=True)
    Fantasy = models.BooleanField(null=True)
    History = models.BooleanField(null=True)
    Horror = models.BooleanField(null=True)
    Music = models.BooleanField(null=True)
    Mystery = models.BooleanField(null=True)
    Romance = models.BooleanField(null=True)
    Science = models.BooleanField(null=True)
    TV  = models.BooleanField(null=True)
    Thriller = models.BooleanField(null=True)
    War = models.BooleanField(null=True)
    Western = models.BooleanField(null=True)
    popularity = models.FloatField(null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()