#coding=utf8

from django.contrib.auth import authenticate,login,logout 
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect

from forms import *
from models import *
from place.models import Relationship,Plan
from blog.models import Article
from django.contrib.auth.models import User

def get_parent_struct(place):
    tmp = place
    place.parent_struct = [tmp,]
    while tmp.parent:
        tmp = tmp.parent
        place.parent_struct.append(tmp)

# @login_required(login_url='/traveller/login/')
def traveller_index(request,user_id):
    traveller = User.objects.get(id=user_id)
    relationships = Relationship.objects.filter(user_id=user_id)
    articles = Article.objects.filter(user_id=user_id)
    plans = Plan.objects.filter(user_id=user_id)
    traveller.profile.sex = Profile.SEX_CHOICES[traveller.profile.sex][1]

    relationships_been = relationships.filter(status=Relationship.BEEN)
    places = [tmp.place for tmp in relationships_been]
    for place in places:
        get_parent_struct(place)

    return render_to_response('traveller/traveller_index.html',context_instance=RequestContext(request,{"traveller":traveller,"relationships":relationships,"articles":articles,"plans":plans,"places":places}))

def login_view(request):    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]   
            password = form.cleaned_data["password"]   
            user = authenticate(username=username, password=password) 
            login(request,user) 
            return HttpResponseRedirect("../"+str(user.id))
    else:
        form = LoginForm() 
    return render_to_response('traveller/login.html',context_instance=RequestContext(request,{"form":form}))

def logout_view(request):  
    logout(request)  
    return login_view(request)

#view函数成功后再提交事务
@transaction.commit_on_success
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]  
            email = form.cleaned_data["email"]  
            password = form.cleaned_data["password"]  
            first_name = form.cleaned_data["first_name"]  
            last_name = form.cleaned_data["last_name"]  
            phone = form.cleaned_data["phone"]
            sex = form.cleaned_data["sex"]
            introduction = form.cleaned_data["introduction"]
            portrait = request.FILES.get('portrait')
            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)  
            user_profile = Profile(user=user,portrait=portrait,phone=phone,introduction=introduction,sex=sex)
            user_profile.save()
            user.save()  
            user = authenticate(username=username, password=password) 
            login(request,user) 
            return HttpResponseRedirect('../../traveller/'+str(user.id)) 
    else:
        form = RegisterForm() 
    return render_to_response('traveller/register.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def modify(request):
    user = request.user
    if request.method == 'POST':
        form = ModifyForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data["username"]  
            user.email = form.cleaned_data["email"]  
            user.password = form.cleaned_data["password"]  
            user.first_name = form.cleaned_data["first_name"]  
            user.last_name = form.cleaned_data["last_name"]  
            user.profile.phone = form.cleaned_data["phone"]
            user.profile.sex = form.cleaned_data["sex"]
            user.profile.introduction = form.cleaned_data["introduction"]
            if request.FILES.get('portrait'):
                user.profile.portrait.delete()
                user.profile.portrait = request.FILES.get('portrait')
            user.save()
            user.profile.save()
            return HttpResponseRedirect('../../traveller/'+str(user.id))
    else:
        form = ModifyForm(initial={"username":user.username,"email":user.email,"first_name":user.first_name,"last_name":user.last_name,"phone":user.profile.phone,"sex":user.profile.sex,"introduction":user.profile.introduction})
    return render_to_response('traveller/register.html',context_instance=RequestContext(request,{"form":form}))