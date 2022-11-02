from django.db import models


# Create your models here.

class Paper(models.Model):
    paper_topic = models.CharField(max_length=255)
    total_marks = models.IntegerField()
    total_section = models.IntegerField()
    total_time = models.IntegerField()


class Section(models.Model):
    section_topic = models.CharField(max_length=255)
    question_type = models.CharField(max_length=255)
    section_marks = models.IntegerField()
    paper = models.ForeignKey("Paper", blank=True, on_delete=models.CASCADE, related_name='paper', null=True)


class Question(models.Model):
    question_statement = models.CharField(max_length=255)
    section = models.ForeignKey("Section", blank=True, on_delete=models.CASCADE, related_name='section', null=True)


class Option(models.Model):
    option = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey("Question", blank=True, on_delete=models.CASCADE, related_name='question', null=True)
