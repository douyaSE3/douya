#coding=utf8

from django import forms 
from tinymce.widgets import TinyMCE

class ArticleForm(forms.Form):
    title = forms.CharField(label=u"标题：")
    content = forms.CharField(label=u"正文：",widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    public = forms.BooleanField(label=u"是否公开",required=False,initial=True)

class CommentForm(forms.Form):
    content = forms.CharField(label=u"你的回应",widget=forms.Textarea(attrs={'cols' : 80,'rows' : 3}))