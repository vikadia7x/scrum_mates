from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.TextField(max_length=100, blank=False)
    last_name = models.TextField(max_length=500, blank=True)
    email = models.EmailField(blank=False)
    dateofbirth = models.DateField(blank=False, default = '1992-01-01')
    username1 = models.TextField(blank=True)
    zipcode = models.TextField(blank=True)