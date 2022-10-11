from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question
from django.utils import timezone
# Create your views here.

def questionCompareByPubDate(question):
    return question.pub_date

def index(request):
    questions = Question.objects.all()
    questions = sorted(questions, key=questionCompareByPubDate)
    return HttpResponse(questions)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)