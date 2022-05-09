from django.http import HttpResponse
from django.shortcuts import  redirect, render
from tournament.utils.md5 import md5
from tournament import models
from django import forms
from tournament.utils.verificationcode import verification_code
from io import BytesIO

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required= True
        )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"form-control"},render_value=True),
        required= True)
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required= True)

    def clean_password(self):
        cleaned_password = md5(self.cleaned_data.get("password"))
        return cleaned_password

def login(request):
    if request.method =="GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form}) 
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code','')
        if code != user_input_code.upper():
            form.add_error('code',"验证码错误")
            return render(request,"login.html",{"form":form})
        #print(form.cleaned_data)
        #print(form.cleaned_data.get('username'),form.cleaned_data.get('password'))
        obj = models.Participant.objects.filter(name=form.cleaned_data.get('username'),password=form.cleaned_data.get('password')).first()
        if  not obj:
            form.add_error("password","用户名或密码错误")
            return render(request,"login.html",{"form":form})
        request.session["info"] = {"id":obj.id,"username":obj.name}
        request.session.set_expiry(60*60*24*7)#7天免登录
        return redirect("/index")
    return render(request,"login.html",{"form":form})

def visitor_login(request):
    request.session["info"] = {"id":'游客',"username":'游客'}
    request.session.set_expiry(60*60*24*7)#7天免登录
    return redirect('/table/?event=1')

def logout(request):
    request.session.clear()
    return redirect("/index/")

def code(request):
    #返回验证码
    img,code_str = verification_code()
    #print("*******************",code_str)
    request.session['image_code'] = code_str
    request.session.set_expiry(60) #设置60秒有效时间
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
