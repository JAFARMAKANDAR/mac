from django.shortcuts import render
from.models import Blogpost

# Create your views here.
from django.http import HttpResponse
def index(request):
    return render(request, 'blog/index.html')

def blogpost(request, id):
    blogpost = Blogpost.objects.filter(id = id)
    print(blogpost)
    return render(request, 'blog/blogpost.html',{'blogpost':blogpost[0]})