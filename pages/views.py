from django.shortcuts import render
from django.http import HttpResponse
#typically do if else statements in the view


def home_view(request,*args, **kwargs):
    #return HttpResponse("<h1>Hello World</h1>")
    print(request)
    print(args,kwargs)
    return render(request, "home.html", {})

def contacts_view(request,*args, **kwargs):
    return render(request, "contacts.html", {})

def about_view(request,*args, **kwargs):
    my_context = {
        "my_text":"This is about us",
        "my_number": 123,
        "my_list": [132,4242,12313]
    }
    return render(request, "about.html", my_context)

def social_view(request,*args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")
