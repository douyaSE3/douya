from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import transaction
import datetime

from models import *
from forms import *

def view_article(request,article_id):
    article = Article.objects.get(id=article_id)
    comments = article.comment_set.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            user_id = request.user.id 
            update_time = datetime.datetime.now()
            comment = Comment(user_id=user_id,content=content,update_time=update_time,article_id=article_id)
            comment.save()
    else:      
        form = CommentForm()

    return render_to_response('blog/view_article.html',context_instance=RequestContext(request,{"article":article,"comments":comments,"comments_num":len(comments),"form":form}))

@transaction.commit_on_success
def add_article(request,place_id):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data["title"]  
            content = form.cleaned_data["content"]  
            public = form.cleaned_data["public"]  
            update_time = datetime.datetime.now()
            article = Article(user_id=user_id,place_id=place_id,title=title,update_time=update_time,content=content,public=public) 
            article.save()  
            return HttpResponseRedirect('../../../../place/'+str(place_id)) 
    else:
        form = ArticleForm()
    return render_to_response('blog/edit_article.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def edit_article(request,article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data["title"]  
            article.content = form.cleaned_data["content"]  
            article.public = form.cleaned_data["public"]  
            article.upload_time = datetime.datetime.now()
            article.save()  
            return HttpResponseRedirect('../../../../place/'+str(article.place.id)) 
    else:
        form = ArticleForm(initial={"title":article.title,"content":article.content,"public":article.public})
    return render_to_response('blog/edit_article.html',context_instance=RequestContext(request,{"form":form}))

@transaction.commit_on_success
def del_article(request,article_id):
    article = Article.objects.get(id=article_id)
    place_id = article.place.id
    article.delete()
    return HttpResponseRedirect('../../../../place/'+str(place_id)) 

