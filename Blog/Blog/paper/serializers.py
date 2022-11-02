from rest_framework import serializers
from .models import *


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    question = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_statement', 'question']


class SectionSerializer(serializers.ModelSerializer):
    section = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'section_topic', 'question_type', 'section_marks', 'section']


class PaperSerializer(serializers.ModelSerializer):
    paper = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Paper
        fields = ['id', 'paper_topic', 'total_marks', 'total_time', 'total_section', 'paper']
