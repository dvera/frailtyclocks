from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='document/')
    resultdoc = models.FileField(upload_to='result/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Agelife(models.Model):
    groupname=models.CharField(max_length=100,blank=True)
    frightmedian = models.FloatField(max_length=50, blank=True)
    frightmean=models.FloatField(max_length=50, blank=True)
    frightstd=models.FloatField(max_length=50, blank=True)
    afraidmedian=models.FloatField(max_length=50, blank=True)
    afraidmean=models.FloatField(max_length=50, blank=True)
    afraidstd=models.FloatField(max_length=50, blank=True)
    frightresult=models.CharField(max_length=1000, blank=True)
    afraidresult=models.CharField(max_length=1000, blank=True)

class Ipdate(models.Model):
    ip=models.CharField(max_length=100, blank=True)
    datetime=models.CharField(max_length=100,blank=True)