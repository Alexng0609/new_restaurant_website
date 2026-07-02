from django.contrib import admin
from .models import NewsFeed, MenuItem, Category
# Register your models here.

admin.site.register(NewsFeed)
admin.site.register(MenuItem)
admin.site.register(Category)
