from django.shortcuts import redirect, render
from tournament import models
from tournament.utils.bootstrap_modelform import BootstrapModelForm
from tournament.utils.pagination import Pagination
from tournament.views.test import update_fakecup_table,update_njcup_table

def schedule(request):
    query_set = models.Game.objects.all()

    page_obj = Pagination(request=request,queryset=query_set,page_size=8,step=2)
    page_queryset = page_obj.page_queryset
    page_string = page_obj.html()

    param_dict = {
        "query_set":page_queryset,
        "page_string":page_string
    }
    return render(request,"schedule.html",param_dict)

class GameModelForm(BootstrapModelForm):
    class Meta:
        model = models.Game
        fields = "__all__"


def game_add(request):
    if request.method == "GET":
        form = GameModelForm()
        param_dict = {
            "form":form,
        }
        return render(request,"game_add.html",param_dict)
    form = GameModelForm(data=request.POST)
    if form.is_valid():  

        if form.cleaned_data.get('home').name == request.session['info'].get('username') or\
            form.cleaned_data.get('away').name == request.session['info'].get('username'):
                form.save()      
        else:
            print("只能登记自己参加的比赛！")
        if form.cleaned_data.get('home').name == form.cleaned_data.get('away').name:
            print("不能自己踢自己！")

        if form.cleaned_data.get('event') == 1:     #更新新旅程杯积分表
            update_njcup_table()
        if form.cleaned_data.get('event') == 2:     #更新不存在的杯积分表
            update_fakecup_table()
            print("updated")
    
    return redirect('/table/?event='+ str(form.cleaned_data.get('event')))

