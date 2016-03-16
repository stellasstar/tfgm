from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('This page shows a list of most recent posts.')


