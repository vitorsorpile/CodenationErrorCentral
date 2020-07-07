from django.shortcuts import render, redirect
from rest_framework import viewsets
from errors.models import Error 
from errors.forms import ErrorForm
from django.db.models.query import QuerySet

from errors.api.serializers import ErrorSerializer
from rest_framework.authtoken.models import Token

# Create your views here.

class ErrorApiViewSet(viewsets.ModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer


def index_view(request, archived=False):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    context = {}
    
    token = Token.objects.get(user = user.pk)
    context['token'] = token

    context['categories'] = [('', 'Selecionar categoria'), ('PRODUÇÃO', 'Produção'),
                             ('HOMOLOGAÇÃO', 'Homologação'), ('DEV', 'Dev')
                            ]
    selectedCategory = None
    
    context['order'] = [('', 'Ordenar por'), ('level', 'Level'),
                        ('date', 'Mais antigo'), ('-date', 'Mais recente'),
                        ('-events', 'Frequência')
                       ]
    selectedOrder = None
    
    context['search'] = [('', 'Buscar por'), ('title', 'Título'),
                         ('description', 'Descrição'), ('address', 'Origem')
                        ]
    selectedSearch = None

    query = ''
    if request.GET:
        selectedCategory = request.GET['category']  
        selectedOrder = request.GET['orderBy']
        selectedSearch = request.GET['searchBy']
        query = request.GET['query']

    context['selectedCategory'] = selectedCategory
    context['selectedOrder'] = selectedOrder
    context['selectedSearch'] = selectedSearch
    context['query'] = query

    errors = get_errors_by_category(selectedCategory).filter(user=user.pk,
                                                        archived=archived)
    errors = get_error_queryset(errors, query, selectedSearch)
    
    if selectedOrder:
        errors = errors.order_by(selectedOrder)

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
            error.address = request.POST['address']
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
        error.archived = not error.archived
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
    if user != error.user:
        return redirect('index')
    
    context['error'] = error
    errorUser = Token.objects.get(user = error.user.pk)
    context['errorUser'] = errorUser
    return render(request, 'error.html', context = context)


def archived_errors_view(request):
    return index_view(request, archived=True)
    

def get_errors_by_category(category=None):
    if category:
        return Error.objects.filter(category=category)
    
    return Error.objects.all()


def get_error_queryset(queryset, query, searchBy=None):
    if not searchBy:
        return queryset
    
    qs = QuerySet(model=Error).none()

    queries = query.split(' ')
    search = searchBy + '__icontains'

    for q in queries:
        errors = queryset.filter(**{search: q})
        qs = qs.union(errors)

    return qs