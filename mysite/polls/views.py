from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from polls.models import Question
from django.utils import timezone
from django.template import loader
from django.shortcuts import render

def questionCompareByPubDate(question):
    return question.pub_date

def index(request):
    questions = Question.objects.all()
    questions = sorted(questions, key=questionCompareByPubDate)

    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': questions,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)