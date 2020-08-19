from django.contrib import admin
from . import models

# Register your models here.

class ReviewInLine(admin.TabularInline):
    model = models.ReviewMember

admin.site.register(models.Review)