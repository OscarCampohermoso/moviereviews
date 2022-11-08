from django.shortcuts import render
from .models import News

def news(request):
    newss = News.objects.all().order_by('-date') # -date means descending order of date field in News model class 
    return render(request, 'news.html',
        {'newss': newss})