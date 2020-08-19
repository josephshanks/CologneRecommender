from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from review.models import Review

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Quiz(models.Model):

    mf = (('Male','Male'),('Female','Female'))
    yn = (('Yes','Yes'),('No','No'))
    toy=(('Winter','Winter'),('Spring','Spring'),('Summer','Summer'),('Autumn','Autumn'))
    tod=(('Day','Day'),('Night','Night'))
    like = (('Females over 25','Females over 25'),('Females under 25','Females under 25'),('Male over 25','Male over 25'),('Male under 25','Male under 25'))
    power = (('close to skin','close to skin'),('arm length','arm length'),('radiate 6ft','radiate 6ft'),('fills the room','fills the room'))
    lasting = (('30 minutes to an hour','30 minutes to an hour'),('1 hour to 2 hours','1 hour to 2 hours'),('3 hours to 6 hours','3 hours to 6 hours'),('7 hours to 12 hours','7 hours to 12 hours'), ('Longer than 12 hours','Longer than 12 hours'))


    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz')
    created_at = models.DateField(auto_now=True)
    sex = models.CharField(max_length=6,choices=mf)
    age = models.DateField()
    signature = models.CharField(max_length=3,choices=yn)
    season = models.TextField(choices=toy)
    day = models.TextField(choices=tod)
    sillage = models.TextField(choices=power)
    longevity = models.TextField(choices=lasting)
    forwhom = models.TextField(choices=like)
    price = models.IntegerField(max_length=10000)
    #result = models.TextField()
    #result_html = models.TextField(editable=False)
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='quiz',null=True,blank=True)


    def __str__(self):
        pass
        #return self.result

    def save(self,*args,**kwargs):
        pass
        #self.result_html = miska.html(self.result)
        #super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('quiz:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','review'] #was result