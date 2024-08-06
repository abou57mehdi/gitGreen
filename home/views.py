from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def faq(request):
    return render(request, 'faq.html')  # Ensure faq.html is present