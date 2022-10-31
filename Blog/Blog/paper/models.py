from django.db import models


# Create your models here.

class Paper(models.Model):
    topic = models.CharField(max_length=255)
    total_marks = models.IntegerField()


class Section(models.Model):
    topic = models.CharField(max_length=255)
    section_type = models.CharField(max_length=255)
    section_marks = models.IntegerField()
    paper = models.ForeignKey("Paper", blank=True, on_delete=models.CASCADE, related_name='paper', null=True)


class MCQ(models.Model):
    question = models.CharField(max_length=255)
    section = models.ForeignKey("Section", blank=True, on_delete=models.CASCADE, related_name='section_mcq', null=True)


class MCQOption(models.Model):
    option = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)
    mcq = models.ForeignKey("MCQ", blank=True, on_delete=models.CASCADE, related_name='mcq', null=True)


class CRO(models.Model):
    question = models.CharField(max_length=255)
    section = models.ForeignKey("Section", blank=True, on_delete=models.CASCADE, related_name='section_cro', null=True)


class ERQ(models.Model):
    question = models.CharField(max_length=255)
    section = models.ForeignKey("Section", blank=True, on_delete=models.CASCADE, related_name='section_erq', null=True)
