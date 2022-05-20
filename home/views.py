from django.shortcuts import render

# Create your views here.


def home(request):
    """
    render Landing page
    """
    return render(request, 'home/index.html',)


def about(request):
    """
    render About page
    """
    return render(request, 'about/about.html',)
