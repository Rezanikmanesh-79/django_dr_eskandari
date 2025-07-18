from django.db import models


class Question(models.Model):
    question_text = models.TextField()
    pub_date = models.DateTimeField("date of pub")

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    vote = models.IntegerField(default=0)