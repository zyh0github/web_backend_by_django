from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('data published')

    def wa_published_rencently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __repr__(self):
        return self.question_text
class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __repr__(self):
        return self.choice_text




class Coding(models.Model):
    text=models.CharField(max_length=10)
    gender=models.IntegerField(unique=True,primary_key=True)


class List(models.Model):
    Number=models.IntegerField(unique=True,blank=False,null=False)
    Gender=models.ForeignKey('Coding',on_delete=models.CASCADE) #在默认的情况下，外键储存的是主表的主键（Primary key）
    