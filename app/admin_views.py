from django.shortcuts import render

def custom_admin(request):
    return render(request, 'templates/animate-image.html')