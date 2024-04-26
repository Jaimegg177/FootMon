from django.db import models

# Create your models here.

class Partido(models.Model):
    date = models.DateField()
    home_team = models.CharField(max_length=70)
    away_team = models.CharField(max_length=70)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    tournament = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    country = models.CharField(max_length=70)
    neutral = models.BooleanField()

class Penaltis(models.Model):
    date=models.DateField()
    home_team=models.CharField(max_length=70)
    away_team=models.CharField(max_length=70)
    winner=models.CharField(max_length=70)
    first_shooter=models.CharField(max_length=100)

class Goleadores(models.Model):
    date=models.DateField()
    home_team=models.CharField(max_length=70)
    away_team=models.CharField(max_length=70)
    team=models.CharField(max_length=70)
    scorer=models.CharField(max_length=100)
    minute=models.IntegerField()
    own_goal=models.BooleanField()
    penalty=models.BooleanField()