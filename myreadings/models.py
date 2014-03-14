from django.db import models

class Publisher(models.Model):
    publisher = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.publisher

class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.CharField(max_length=4)     # Year
    description = models.TextField()
    ebook = models.BooleanField()
    page_count = models.IntegerField()
    thumbnail = models.URLField()
    isbn = models.CharField(max_length=15)
    google_id = models.CharField(max_length=15)
    currently_reading = models.BooleanField()
    publisher = models.ForeignKey(Publisher)
    
    def __unicode__(self):
        return self.title
    
class Author(models.Model):
    author = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)
    
    def __unicode__(self):
        return self.author

class Magazine(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.CharField(max_length=4)
    month = models.IntegerField()                       # I divide magazine by months
    number = models.IntegerField()
    thumbnail = models.URLField()
    
    def __unicode__(self):
        return self.title

class Wish(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.title

class ReadRate(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    rate = models.IntegerField()
    book = models.ForeignKey(Book)