from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def Med_Name(request, med_id):
    return HttpResponse("Medicine ID is: %s." %med_id)

def Med_Detail(request, med_id):
    response = "You're looking at medicine %s."
    return HttpResponse(response % med_id)

