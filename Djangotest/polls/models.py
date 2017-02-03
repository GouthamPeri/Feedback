from __future__ import unicode_literals

from django.db import models
class Reporter1(models.Model):
    name = models.CharField(max_length=70,default="1")
    age = models.IntegerField(default=1);
    def __str__(self): # __unicode__ on Python 2
        return self.name

class Rep1(models.Model):
    fname=models.ForeignKey(Reporter1)
    sex=models.CharField(max_length=6)
    def __str__(self): # __unicode__ on Python 2
        return self.fname.name
    '''
class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    def __str__(self): # __unicode__ on Python 2
        return self.headline'''