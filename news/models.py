from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField()
    def __str__(self): # This method is used to display the headline of the news in the admin panel
        # the __str__ method method in Python represents the object as a string
        return self.headline # This is the string representation of the News model class