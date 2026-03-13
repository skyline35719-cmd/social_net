from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
#def index(request):
#    return HttpResponse('Main page')

def index(request):
    template = 'temp.html'
    title = 'Anfisa for friends'
    context = {
        'title': title,
        'text' : 'Main page'
    }
    return render(request, template, context)
