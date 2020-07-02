from django.shortcuts import render, redirect
from rest_framework import viewsets
from errors.models import Error 
from errors.forms import ErrorForm

from errors.api.serializers import ErrorSerializer
from rest_framework.authtoken.models import Token

# Create your views here.

class ErrorApiViewSet(viewsets.ModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer

def index_view(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    context = {}
    
    token = Token.objects.get(user = user.pk)
    context['token'] = token
    errors = Error.objects.filter(user = user.pk, archived=False)

    context['errors'] = errors

    return render(request, 'index.html', context=context)


def add_error_view(request):
    user = request.user
    
    if not user.is_authenticated:
        return redirect('login')

    context = {}
    token = Token.objects.get(user = user.pk)
    context['token'] = token

    if request.POST:
        form = ErrorForm(request.POST)
        if form.is_valid:
            error = Error()
            error.title = request.POST['title']
            error.category = request.POST['category']
            error.level = request.POST['level']
            error.description = request.POST['description']
            error.user = user
            error.save()

            return redirect('index')

        else:
            context['form'] = form
    else:
        form = ErrorForm()
        context['form'] = form
        
    return render(request, 'addError.html', context=context)


def delete_error_view(request, error_id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    error = Error.objects.get(pk = error_id)
    if user == error.user:
        error.delete()

    return redirect('index')


def archive_error_view(request, error_id):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    error = Error.objects.get(pk = error_id)
    if user == error.user:
        error.archived = True
        error.save()
    
    return redirect('index')

def detail_error_view(request, error_id):
    user = request.user

    context = {}
    token = Token.objects.get(user = user.pk)
    context['token'] = token

    if not user.is_authenticated:
        return redirect('login')

    error = Error.objects.get(pk = error_id)
    # if user != error.user:
    #     return redirect('index')
    
    context['error'] = error
    errorUser = Token.objects.get(user = error.user.pk)
    context['errorUser'] = errorUser
    return render(request, 'error.html', context = context)


def archived_errors_view(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    context = {}

    token = Token.objects.get(user = user.pk)
    context['token'] = token
    
    errors = Error.objects.filter(archived=True)
    context['errors'] = errors
    return render(request, 'index.html', context=context)