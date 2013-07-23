#coding=utf8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db import transaction
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
import datetime
from django.utils.timezone import utc
from django.utils import simplejson as json
import os
from blog.forms import CommentForm

from models import *
from forms import *

def get_parent_struct(place):
    tmp = place
    tmp.children = tmp.place_set.all()
    place.parent_struct = [tmp,]
    while tmp.parent:
        tmp = tmp.parent
        tmp.children = tmp.place_set.all()
        place.parent_struct.append(tmp)

def index(request):
    asia = Place.objects.filter(parent_id=100001)[:8]
    for place in asia:
        place.children = place.place_set.all()[:6]
    africa = Place.objects.filter(parent_id=110557)[:8]
    for place in africa:
        place.children = place.place_set.all()[:6]
    europe = Place.objects.filter(parent_id=103697)[:8]
    for place in europe:
        place.children = place.place_set.all()[:6]
    oceania = Place.objects.filter(parent_id=113457)[:8]
    for place in oceania:
        place.children = place.place_set.all()[:6]
    northamerica = Place.objects.filter(parent_id=110996)[:8]
    for place in northamerica:
        place.children = place.place_set.all()[:6]
    southamerica = Place.objects.filter(parent_id=113080)[:8]
    for place in southamerica:
        place.children = place.place_set.all()[:6]
    antarctica = Place.objects.filter(parent_id=114283)[:8]
    for place in antarctica:
        place.children = place.place_set.all()[:6]
    return render_to_response('index.html',context_instance=RequestContext(request,locals()))

def place_index(request):
    return render_to_response('place/place_index.html',context_instance=RequestContext(request))

def place_intro(request,place_id):
    place = Place.objects.get(id=place_id)
    parent = place.parent
    children = place.place_set.all()[:16]
    relationship = Relationship.objects.filter(place_id=place_id)
    photos = place.photo_set.all()
    articles = place.article_set.all()
    plans = [play.plan for play in place.play_set.all()]

    for child in children:
        child.want = len(Relationship.objects.filter(status=Relationship.WANT,place_id=child.id))
        child.been = len(Relationship.objects.filter(status=Relationship.BEEN,place_id=child.id))
        child.being = len(Relationship.objects.filter(status=Relationship.BEING,place_id=child.id))
        sum = (len(Relationship.objects.filter(rank=Relationship.ONE,place_id=child.id))+len(Relationship.objects.filter(rank=Relationship.TWO,place_id=child.id))+len(Relationship.objects.filter(rank=Relationship.THREE,place_id=child.id))+len(Relationship.objects.filter(rank=Relationship.FOUR,place_id=child.id))+len(Relationship.objects.filter(rank=Relationship.FIVE,place_id=child.id)))
        if sum!=0:
            child.avg_of_rank = (0.0+1*len(Relationship.objects.filter(rank=Relationship.ONE,place_id=child.id))+2*len(Relationship.objects.filter(rank=Relationship.TWO,place_id=child.id)) +3*len(Relationship.objects.filter(rank=Relationship.THREE,place_id=child.id)) +4*len(Relationship.objects.filter(rank=Relationship.FOUR,place_id=child.id)) +5*len(Relationship.objects.filter(rank=Relationship.FIVE,place_id=child.id)))/sum
        else:
            child.avg_of_rank = 0

    get_parent_struct(place)
    for child in children:
        get_parent_struct(child)

    relationship_info = {}

    relationship_info['want'] = len(relationship.filter(status=Relationship.WANT))
    relationship_info['been'] = len(relationship.filter(status=Relationship.BEEN))
    relationship_info['being'] = len(relationship.filter(status=Relationship.BEING))  

    relationship_info['num_of_1star'] = len(relationship.filter(rank=Relationship.ONE)) 
    relationship_info['num_of_2star'] = len(relationship.filter(rank=Relationship.TWO))
    relationship_info['num_of_3star'] = len(relationship.filter(rank=Relationship.THREE))
    relationship_info['num_of_4star'] = len(relationship.filter(rank=Relationship.FOUR))
    relationship_info['num_of_5star'] = len(relationship.filter(rank=Relationship.FIVE))

    relationship_info['num_of_rank'] = relationship_info['num_of_1star']+relationship_info['num_of_2star']+relationship_info['num_of_3star']+relationship_info['num_of_4star']+relationship_info['num_of_5star']
    if relationship_info['num_of_rank'] != 0:
        relationship_info['per_of_1star'] = (100*relationship_info['num_of_1star']+0.0)/relationship_info['num_of_rank']
        relationship_info['per_of_2star'] = (100*relationship_info['num_of_2star']+0.0)/relationship_info['num_of_rank']
        relationship_info['per_of_3star'] = (100*relationship_info['num_of_3star']+0.0)/relationship_info['num_of_rank']
        relationship_info['per_of_4star'] = (100*relationship_info['num_of_4star']+0.0)/relationship_info['num_of_rank']
        relationship_info['per_of_5star'] = (100*relationship_info['num_of_5star']+0.0)/relationship_info['num_of_rank']
        relationship_info['avg_of_rank'] = (1*relationship_info['per_of_1star']+2*relationship_info['per_of_2star']+3*relationship_info['per_of_3star']+4*relationship_info['per_of_4star']+5*relationship_info['per_of_5star'])/100
    else:
        relationship_info['avg_of_rank'] = False

    relationship_info['info'] = False
    try:
        if relationship.get(user_id=request.user.id):
            r = relationship.get(user_id=request.user.id)
            relationship_info['status'] = Relationship.STATUS_CHOICES[r.status][1]
            relationship_info['text'] = r.text
            relationship_info['date'] = r.date
            if r.rank is not None:
                relationship_info['rank'] = r.rank
            relationship_info['info'] = True
    except Exception, e:
        # print e
        pass

    return render_to_response('place/place_intro.html',context_instance=RequestContext(request,{"place":place,"plans":plans,"parent":parent,"children":children,"relationship_info":relationship_info,"photos":photos,"articles":articles}))

def place_search(request):
    q = request.GET.get('q')
    results = []
    returnall =[]
    if q:  
        results.extend(Place.objects.filter(chinese_name__icontains=q))
        results.extend(Place.objects.filter(english_name__icontains=q))

    result_num=0
    for result in results:
        result_num=result_num+1
        relationship = Relationship.objects.filter(place_id=result.id)
        relationship_info = {}

        relationship_info['place'] = result
        relationship_info['want'] = len(relationship.filter(status=Relationship.WANT))
        relationship_info['been'] = len(relationship.filter(status=Relationship.BEEN))
        relationship_info['being'] = len(relationship.filter(status=Relationship.BEING))  

        relationship_info['num_of_1star'] = len(relationship.filter(rank=Relationship.ONE)) 
        relationship_info['num_of_2star'] = len(relationship.filter(rank=Relationship.TWO))
        relationship_info['num_of_3star'] = len(relationship.filter(rank=Relationship.THREE))
        relationship_info['num_of_4star'] = len(relationship.filter(rank=Relationship.FOUR))
        relationship_info['num_of_5star'] = len(relationship.filter(rank=Relationship.FIVE))

        relationship_info['num_of_rank'] = relationship_info['num_of_1star']+relationship_info['num_of_2star']+relationship_info['num_of_3star']+relationship_info['num_of_4star']+relationship_info['num_of_5star']
        if relationship_info['num_of_rank'] != 0:
            relationship_info['per_of_1star'] = (100*relationship_info['num_of_1star']+0.0)/relationship_info['num_of_rank']
            relationship_info['per_of_2star'] = (100*relationship_info['num_of_2star']+0.0)/relationship_info['num_of_rank']
            relationship_info['per_of_3star'] = (100*relationship_info['num_of_3star']+0.0)/relationship_info['num_of_rank']
            relationship_info['per_of_4star'] = (100*relationship_info['num_of_4star']+0.0)/relationship_info['num_of_rank']
            relationship_info['per_of_5star'] = (100*relationship_info['num_of_5star']+0.0)/relationship_info['num_of_rank']
            relationship_info['avg_of_rank'] = (1*relationship_info['per_of_1star']+2*relationship_info['per_of_2star']+3*relationship_info['per_of_3star']+4*relationship_info['per_of_4star']+5*relationship_info['per_of_5star'])/100
        else:
            relationship_info['avg_of_rank'] = False

        relationship_info['info'] = False
        returnall.append(relationship_info)
    return render_to_response('place/place_search.html',context_instance=RequestContext(request,{"results":returnall,"search_string":q,"result_num":result_num}))

@transaction.commit_on_success
def add_relationship(request,place_id,operation):
    if request.method == 'POST':
        form = RelationshipForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            status = form.cleaned_data["status"]  
            date = form.cleaned_data["date"]  
            rank = form.cleaned_data["rank"]  
            text = form.cleaned_data["text"]  
            if rank:
                relationship = Relationship(user_id=user_id,place_id=place_id,status=status,date=date,rank=rank,text=text) 
            else:
                relationship = Relationship(user_id=user_id,place_id=place_id,status=status,date=date,text=text) 
            relationship.save()  
            return HttpResponse(json.dumps({"success":True}),mimetype="application/json")
    else:
        form = RelationshipForm(initial={'status':operation})
    return render_to_response('place/relationship.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def del_relationship(request,place_id):
    user_id = request.user.id
    relationship = Relationship.objects.get(place_id=place_id,user_id=user_id)
    relationship.delete()
    return HttpResponse(json.dumps({"success":True}),mimetype="application/json")

@transaction.commit_on_success
def modify_relationship(request,place_id):
    user_id = request.user.id
    relationship = Relationship.objects.get(place_id=place_id,user_id=user_id)
    if request.method == 'POST':
        form = RelationshipForm(request.POST)
        if form.is_valid():
            relationship.status = form.cleaned_data["status"]  
            relationship.date = form.cleaned_data["date"]  
            if form.cleaned_data["rank"]:
                relationship.rank = form.cleaned_data["rank"]  
            relationship.text = form.cleaned_data["text"] 
            relationship.save()  
            return HttpResponse(json.dumps({"success":True}),mimetype="application/json")
    else:       
        form = RelationshipForm(initial={'status':relationship.status,'date':relationship.date,'rank':relationship.rank,'text':relationship.text})
    return render_to_response('place/relationship.html',context_instance=RequestContext(request,{"form":form}))

def view_plan(request,plan_id):
    plan = Plan.objects.get(id=plan_id)
    photos = plan.photo_set.all()
    plays = plan.play_set.all().order_by('order')
     
    for play in plays:    
        get_parent_struct(play.place)
        if hasattr(play,'prev'):
            play.prev.transportation_name = Route.TRANS_CHOICES[play.prev.transportation][1] 

    return render_to_response('place/view_plan.html',context_instance=RequestContext(request,{"plan":plan,"photos":photos,"plays":plays}))


@transaction.commit_on_success
def add_photo(request,plan_id):
    plan = Plan.objects.get(id=plan_id)
    plays = plan.play_set.all()
    q = Q()
    for play in plays:
        tmp = Q(id=play.place_id)
        q = q|tmp
    place_set = Place.objects.filter(q)
    if request.method == 'POST':
        form = PhotoForm(place_set=place_set,data=request.POST,files=request.FILES)
        if form.is_valid():
            place = form.cleaned_data["place"]
            image = request.FILES['image']  
            title = form.cleaned_data["title"]  
            description = form.cleaned_data["description"]  
            now = datetime.datetime.utcnow().replace(tzinfo=utc) 
            photo = Photo(place_id=place.id,image=image,title=title,description=description,plan_id=plan_id,upload_time=now)
            photo.save()
            return HttpResponse(json.dumps({"success":True}),mimetype="application/json")
    else:      
        form = PhotoForm(place_set=place_set)
    return render_to_response('place/photo.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def del_photo(request,photo_id):
    photo = Photo.objects.get(id=photo_id)
    plan_id = photo.plan.id
    photo.image.delete()
    photo.delete()
    return HttpResponse(json.dumps({"success":True}),mimetype="application/json")

@transaction.commit_on_success
def add_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data["title"] 
            public = form.cleaned_data["public"] 
            plan = Plan(user_id=user_id,title=title,public=public) 
            plan.save()  
            return HttpResponse(json.dumps({"success":True,"plan_id":plan.id}),mimetype="application/json")
    else:
        form = PlanForm()
    return render_to_response('place/add_plan.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def copy_plan(request,origin_plan_id):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data["title"] 
            public = form.cleaned_data["public"] 
            new_plan = Plan(user_id=user_id,title=title,public=public) 
            new_plan.save()  

            origin_plan = Plan.objects.get(id=origin_plan_id)
            for play in origin_plan.play_set.all():
                new_play = Play(plan_id=new_plan.id,place_id=play.place.id,begin_time=play.begin_time,end_time=play.end_time,tips=play.tips,cost=play.cost,order=play.order)
                new_play.save()
                if hasattr(play,'prev'):
                    route = play.prev
                    new_route = Route(end_play_id=new_play.id,plan_id=new_plan.id,transportation=route.transportation,begin_time=route.begin_time,end_time=route.end_time,tips=route.tips,cost=route.cost)
                    new_route.save()
            return HttpResponse(json.dumps({"success":True,"plan_id":new_plan.id}),mimetype="application/json")
    else:
        form = PlanForm()
    return render_to_response('place/add_plan.html',context_instance=RequestContext(request,{"form":form}))

def edit_plan(request,plan_id):
    plan = Plan.objects.get(id=plan_id)
    plays = plan.play_set.all().order_by('order')
    for play in plays:
        if hasattr(play,'prev'):
            play.prev.transportation_name = Route.TRANS_CHOICES[play.prev.transportation][1] 
	
    for place in [play.place for play in plays]:    
        get_parent_struct(place)

    return render_to_response('place/edit_plan.html',context_instance=RequestContext(request,{"plan":plan,"plays":plays}))

def edit_plan_search(request):
    q = request.GET.get('q')
    query = Q(chinese_name__icontains=q)|Q(english_name__icontains=q)
    places = Place.objects.filter(query)
     
    if places:
        results = []
        for place in places:
            get_parent_struct(place)
            result = {}
            result['name'] = place.__unicode__()
            result['description'] = place.description
            result['id'] = place.id
            result['has_img'] = place.has_img
            result['parent_struct'] = []
            for parent in place.parent_struct:
                tmp={}
                tmp['chinese_name'] = parent.chinese_name
                tmp['english_name'] = parent.english_name
                result['parent_struct'].append(tmp)
            results.append(result)
    else:
        results = False
    return HttpResponse(json.dumps({"results":results}),mimetype="application/json")

@transaction.commit_on_success
def add_play(request,plan_id):
    place_id = request.POST.get('id')
    plan = Plan.objects.get(id=plan_id)
    for play in plan.play_set.all():
        if str(play.place.id) == place_id:
            result = False
            return HttpResponse(json.dumps({"result":result}),mimetype="application/json")
    result = {}
    play = Play(plan_id=plan_id,place_id=place_id)

    get_parent_struct(play.place)

    result['name'] = play.place.__unicode__()
    result['parent_struct'] = []
    for parent in play.place.parent_struct:
        tmp={}
        tmp['chinese_name'] = parent.chinese_name
        tmp['english_name'] = parent.english_name
        result['parent_struct'].append(tmp)
    play.save()
    result['id'] = play.id
  
    if len(Play.objects.filter(plan_id=plan_id)) != 1:
        route = Route(plan_id=plan_id,end_play_id=play.id)
        route.save()
        result['route_id'] = route.id
    else:
        result['route_id'] = False

    return HttpResponse(json.dumps({"result":result}),mimetype="application/json")

@transaction.commit_on_success
def edit_play(request,play_id):
    play = Play.objects.get(id=play_id)
    if request.method == 'POST':
        form = PlayForm(request.POST)
        if form.is_valid():
            play.tips = form.cleaned_data.get("tips")
            play.cost= form.cleaned_data.get("cost")
            play.begin_time = form.cleaned_data.get("begin_time")
            play.end_time = form.cleaned_data.get("end_time")
            play.save()
            return HttpResponse(json.dumps({"success":True}),mimetype="application/json")
    else:       
        form = PlayForm(initial={"tips":play.tips,"cost":play.cost,"begin_time":play.begin_time,"end_time":play.end_time})
    return render_to_response('place/play.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def del_play(request,play_id):
    play = Play.objects.get(id=play_id)
    has_prev = hasattr(play,'prev')
    play.delete()
    return HttpResponse(json.dumps({"success":True,"has_prev":has_prev,"play_id":play_id}),mimetype="application/json")

@transaction.commit_on_success
def edit_route(request,route_id):
    route = Route.objects.get(id=route_id)
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route.tips = form.cleaned_data.get("tips")
            route.cost= form.cleaned_data.get("cost")
            route.begin_time = form.cleaned_data.get("begin_time")
            route.end_time = form.cleaned_data.get("end_time")
            route.transportation = form.cleaned_data.get("transportation")
            route.save()
            transportation_name = Route.TRANS_CHOICES[int(route.transportation)][1] 
            return HttpResponse(json.dumps({"success":True,"id":route.id,"transportation":route.transportation,"transportation_name":transportation_name}),mimetype="application/json")
    else:       
        form = RouteForm(initial={"tips":route.tips,"cost":route.cost,"begin_time":route.begin_time,"end_time":route.end_time,"transportation":route.transportation})
    return render_to_response('place/route.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def del_route(request,route_id):
    route = Route.objects.get(id=route_id)
    route.delete()
    return HttpResponse(json.dumps({"success":True}),mimetype="application/json")
