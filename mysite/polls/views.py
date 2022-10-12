from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from polls.models import Question, Choice
from django.utils import timezone
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

def questionCompareByPubDate(question):
    return question.pub_date

def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now())
    questions = sorted(questions, key=questionCompareByPubDate)
    
    questions_out = []
    for question in questions:
        if question.choice_set.exists():
            questions_out.append(question)
    
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': questions_out,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))