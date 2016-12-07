from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import  Question,Choice
from  django.http import Http404
# Create your views here.
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return  render(request,'polls/index.html',context)

def detail(reuqust,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return  render(reuqust,'polls/detail.html',{'question':question})

def results(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(requset,question_id):
    p=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=p.choice_set.get(pk=requset.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return  render(requset,'polls/detail.html',{
            'question':p,
            'error_message':"you didn`t select a choice"
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return  HttpResponseRedirect(reversed('polls:results',args=(p.id,)))