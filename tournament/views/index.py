from django.shortcuts import render
from tournament import models

def index(request):
    njcup_top_3 = models.NewJourneyCup.objects.all().order_by('current_rank')[0:3]
    #fakecup_top_3 = models.FakeCup.objects.all().order_by('current_rank')[0:3]
    param_dict = {
        "njcup_top_3":njcup_top_3,
        #"fakecup_top_3":fakecup_top_3,
    }
    return render(request,'index.html',param_dict)

def intro(request):
    return render(request,'intro.html')