from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context,Template




# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = Context()
    return HttpResponse(template.render(context))
