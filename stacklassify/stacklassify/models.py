from django.db import models
from django.db.models import Count
from random import randint
import uuid


class JobManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('guid'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
    def random_new(self,Person):
        count = self.exclude(classified_by=Person).aggregate(count=Count('guid'))['count']
        random_index = randint(0, count - 1)
        return self.exclude(classified_by=Person)[random_index]

class Person(models.Model):
    id = models.CharField(max_length=200,
                          blank=True,unique=True,default=uuid.uuid4,primary_key=True)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200,default="")

class Job(models.Model):
    guid = models.CharField(max_length=200,primary_key=True)
    title = models.CharField(max_length=200)
    classified_by = models.ManyToManyField(Person)
    objects = JobManager()

class JobClassification(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    classification = models.BooleanField()
    duration_looked_at = models.FloatField(default=0)
    text_reached = models.CharField(max_length=200,default="")
    whats_wrong = models.CharField(max_length=200,default="")

