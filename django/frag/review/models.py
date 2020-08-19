from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# might not need
from django import template
register = template.Library()

class Review(models.Model):
    name = models.CharField(max_length=500,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    rating = models.IntegerField(blank=True,choices=((1,1),(2,2),(3,3),(4,4),(5,5)))
    # rating_html = models.IntegerField
    average = models.ManyToManyField(User,through='ReviewMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #self.rating_html = misaka.html(self.rating)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('review:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class ReviewMember(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='reviewer')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_review')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('review','user')