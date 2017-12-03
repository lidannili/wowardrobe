from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from random import randint

# Create your models here.
class UserProfile(models.Model):
    image = models.ImageField(upload_to='profile_image', blank=True, default='profile_image/profile_placeholder.png')
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email_confirm = models.BooleanField(default=False)
    user = models.OneToOneField(User)
    date_of_birth = models.DateField()
    height = models.FloatField(blank=True,null=True)
    weight = models.FloatField(blank=True,null=True)
    budget = models.FloatField(blank=True,null=True)

    # def __str__(self):
    #     return self.user.name + ',' + self.user.email

# class Closet(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255, blank=True)
#     # user = models.ForeignKey(UserProfile)

    # def __str__(self):
    #     return self.name + ',' + self.description

class Clothes(models.Model):
    name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='clothes_image')
    category = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=255, blank=True)
    style = models.CharField(max_length=255, blank=True)
    event = models.CharField(max_length=255, blank=True)
    season = models.CharField(max_length=255, blank=True)
    weather = models.CharField(max_length=255, blank=True)
    temperature_level = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name + ',' + self.user.username

    def random(self, params, user):
        count = self.objects.filter(category__contains=params, user=user).aggregate(count=Count('id'))['count']
        if count == 0:
            return 0
        if count == 1:
            random_index = 0
        else:
            random_index = randint(0, count - 1)
        return self.objects.filter(category__contains=params, user=user)[random_index]

class Tags(models.Model):
    tagname = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    clothes = models.ForeignKey(Clothes)
    category = models.CharField(max_length=10, default='')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.tagname + self.type + self.clothes.id

class Outfits(models.Model):
    name = models.CharField(max_length=200, blank=True)
    counts = models.IntegerField(default=0, blank=True)
    top1 = models.ForeignKey(Clothes, related_name='top1' ,blank=True, null=True)
    top2 = models.ForeignKey(Clothes, related_name='top2', blank=True, null=True)
    bottom = models.ForeignKey(Clothes, related_name='bottom', blank=True, null=True)
    shoes = models.ForeignKey(Clothes, related_name='shoes', blank=True, null=True)
    dress = models.ForeignKey(Clothes, related_name='dress', blank=True, null=True)
    temperature_level = models.IntegerField(blank=True, default=-1)
    style = models.CharField(max_length=255, blank=True)
    event = models.CharField(max_length=255, blank=True)
    season = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name +self.counts + self.last_date + self.isFavorite

class DailyOutfit(models.Model):
    user = models.OneToOneField(User,null= True)
    today = models.ForeignKey(Outfits, blank = True, null=True,related_name='today')
    tomorrow = models.ForeignKey(Outfits, blank = True,null=True, related_name='tomorrow')

    def __str__(self):
        return self.today + ',' + self.tomorrow + self.user

