from rest_framework import viewsets
from rest_framework.response import Response
import docx2txt
from .serializers import *
from .utils import *


# Create your views here.

class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def create(self, request, *args, **kwargs):
        text = docx2txt.process(request.FILES['paper'])
        paper = parsed_data(text)
        paper_serializer = PaperSerializer(data={"paper_topic": paper["paper_detail"]["topic"],
                                                 "total_marks": paper["paper_detail"]["total_marks"],
                                                 "total_section": len(paper["section_detail"]),
                                                 "total_time": paper["paper_detail"]["total_time"]}, partial=True)

        if paper_serializer.is_valid():
            paper_serializer_ = paper_serializer.save()

        for section in paper["section_detail"]:
            section_serializer = SectionSerializer(data={"section_topic": section["section_topic"],
                                                         "question_type": section["question_type"],
                                                         "section_marks": section["section_marks"]},
                                                   partial=True)

            if section_serializer.is_valid():
                section_serializer_ = section_serializer.save()

            if section["question_type"] == "MCQs":
                for mcq in paper["mcq"]:
                    question_serializer = QuestionSerializer(data={"question_statement": mcq["question"]},
                                                             partial=True)
                    if question_serializer.is_valid():
                        question_serializer_ = question_serializer.save()

                    for option in mcq["option"]:
                        option_serializer = OptionSerializer(data={"option": option[0], "is_true": option[1]})

                        if option_serializer.is_valid():
                            option = option_serializer.save()
                            question_serializer_.question.add(option)
                            question_serializer_.save()
                            section_serializer_.section.add(question_serializer_)

            if section["question_type"] == "CRQ":
                for crq in paper["crq"]:
                    question_serializer = QuestionSerializer(data={"question_statement": crq},
                                                             partial=True)
                    if question_serializer.is_valid():
                        question_serializer_ = question_serializer.save()
                        section_serializer_.section.add(question_serializer_)

            if section["question_type"] == "ERQ":
                for erq in paper["erq"]:
                    question_serializer = QuestionSerializer(data={"question_statement": erq},
                                                             partial=True)
                    if question_serializer.is_valid():
                        question_serializer_ = question_serializer.save()
                        section_serializer_.section.add(question_serializer_)

            section_serializer_.save()
            paper_serializer_.paper.add(section_serializer_)
            paper_serializer_.save()
        return Response(status=200)
