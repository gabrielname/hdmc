from django.shortcuts import redirect, render
from tournament.utils.bootstrap_modelform import BootstrapModelForm
from tournament import models

class ParticipantModelForm(BootstrapModelForm):
    class Meta:
        model = models.Participant
        fields = ["name",'qq','gender','type_of_team','highest_rank']

def participant_add(request):
    if request.method == "GET":
        form = ParticipantModelForm()
        return render(request,"participant_add.html",{"form":form})
    form = ParticipantModelForm(data=request.POST)
    if form.is_valid():
        form.save()
    
    #计算更新所有选手排名
    # players = models.Participant.objects.all().order_by('-points')
    # i = 1
    # for p in players:
    #     models.Participant.objects.filter(id=p.id).update(current_rank=i)
    #     i = i + 1

    return redirect("/table")

def participant_delete(request):
    pid = request.GET.get('pid')
    models.Participant.objects.filter(id=pid).delete()

    #计算更新所有选手排名
    players = models.Participant.objects.all().order_by('-points')
    i = 1
    for p in players:
        models.Participant.objects.filter(id=p.id).update(current_rank=i)
        i = i + 1

    return redirect("/table")

def participant_information(request):

    return render(request,"participant_information.html")