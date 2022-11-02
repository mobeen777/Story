import re
import docx2txt
from .models import *
from .constants import (PAPER_TOPIC_PATTERN, PAPER_MARKS_PATTERN, TOTAL_TIME_PATTERN, QUESTION_TYPE_PATTERN,
                        SECTION_MARKS_PATTERN, SECTION_TOPIC_PATTERN, MCQ_SECTION_PATTERN, CRQ_SECTION_PATTERN,
                        ERQ_SECTION_PATTERN)


def topic_marks_time(text):
    topic = re.findall(PAPER_TOPIC_PATTERN, text)
    total_marks = re.findall(PAPER_MARKS_PATTERN, text)
    total_time = re.findall(TOTAL_TIME_PATTERN, text)
    time = 0
    if total_time[0].find(':') == -1:
        time = int(total_time[0]) * 60000
        print(1)
    else:
        time = total_time[0].split(':')
        time = (int(time[0]) * 3600000) + (int(time[1]) * 60000)
        print(2)

    topic_total_marks_time = {
        'topic': topic[0].strip(),
        'total_marks': int(total_marks[0]),
        'total_time': time,
    }

    return topic_total_marks_time


def sections_marks_topic(text):
    sections_type = re.findall(QUESTION_TYPE_PATTERN, text)
    marks = re.findall(SECTION_MARKS_PATTERN, text)
    topics = re.findall(SECTION_TOPIC_PATTERN, text)

    section_mark_topic = []
    for i in range(len(sections_type)):
        section_mark_topic.append({'question_type': sections_type[i],
                                   'section_marks': int(marks[i]),
                                   'section_topic': topics[i]})

    return section_mark_topic


def mcq_questions(text):
    mcq_section = re.findall(MCQ_SECTION_PATTERN, text)
    all_mcq = mcq_section[0][0].split("\n\n")

    # Removing Empty  Strings
    all_mcq = [i for i in all_mcq if i]

    mcq_question_options = []
    for i in range(2, len(all_mcq), 5):
        question = i
        options = []

        for j in range(4):
            i += 1
            if i < len(all_mcq):
                if all_mcq[i][0] == '*':
                    all_mcq[i] = all_mcq[i][1:]
                    options.append((all_mcq[i], True))
                else:
                    options.append((all_mcq[i], False))
        mcq_question_options.append({
            'question': all_mcq[question],
            'option': options
        })
    return mcq_question_options


def crq_question(text):
    crq_section = re.findall(CRQ_SECTION_PATTERN, text)
    crq = crq_section[0][0].split("\n\n")

    # Removing Empty  Strings
    crq = [i for i in crq if i]

    all_crq = []
    for question_no in range(2, len(crq)):
        all_crq.append(crq[question_no])

    return all_crq


def erq_question(text):
    erq_section = re.findall(ERQ_SECTION_PATTERN, text)
    erq = erq_section[0][0].split("\n\n")

    # Removing Empty  Strings
    erq = [i for i in erq if i]

    all_erq = []
    question_no = 2
    # for question_no in range(2, len(erq)):
    while question_no < len(erq):
        print(question_no, 2)
        if question_no == len(erq) - 1:
            if erq[question_no].find('Topic: ') == -1:
                all_erq.append(erq[question_no])
                break
            else:
                break
        elif erq[question_no + 1].find('Topic: ') != -1:
            erq[question_no] = erq[question_no] + erq[question_no + 1]
            all_erq.append(erq[question_no])
            question_no += 1
            print(question_no, 1)
        else:
            all_erq.append(erq[question_no])
        question_no += 1
    return all_erq


def parsed_data(text):
    paper_detail = topic_marks_time(text)
    section_details = sections_marks_topic(text)
    mcq = mcq_questions(text)
    crq = crq_question(text)
    erq = erq_question(text)

    return {'paper_detail': paper_detail,
            'section_detail': section_details,
            'mcq': mcq,
            'crq': crq,
            'erq': erq}


def save_paper(paper_docx):
    text = docx2txt.process(paper_docx)
    paper = parsed_data(text)
    paper_object = Paper.objects.create(paper_topic=paper["paper_detail"]["topic"],
                                        total_marks=paper["paper_detail"]["total_marks"],
                                        total_section=len(paper["section_detail"]),
                                        total_time=paper["paper_detail"]["total_time"])
    for section in paper["section_detail"]:
        section_object = Section.objects.create(paper=paper_object, section_topic=section["section_topic"],
                                                question_type=section["question_type"],
                                                section_marks=section["section_marks"]
                                                )
        if section["question_type"] == "MCQs":
            for mcq in paper["mcq"]:
                question_object = Question.objects.create(section=section_object,
                                                          question_statement=mcq["question"])

                for option in mcq["option"]:
                    option_object = Option.objects.create(question=question_object, option=option[0],
                                                          is_true=option[1])
                    option_object.save()
                question_object.save()
        if section["question_type"] == "CRQ":
            for crq in paper["crq"]:
                question_object = Question.objects.create(section=section_object, question_statement=crq)
                question_object.save()
        if section["question_type"] == "ERQ":
            for erq in paper["erq"]:
                question_object = Question.objects.create(section=section_object, question_statement=erq)
                question_object.save()

        section_object.save()
    paper_object.save()
