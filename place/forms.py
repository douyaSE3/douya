#coding=utf8

from django import forms 
from models import *
from django.contrib.admin import widgets

class RelationshipForm(forms.Form):
    status = forms.ChoiceField(label=u"",widget=forms.RadioSelect,choices=Relationship.STATUS_CHOICES)
    date = forms.DateField(label=u"出游日期",widget=widgets.AdminDateWidget(attrs={'size': 20,}),required=False)
    rank = forms.ChoiceField(label=u"给个评价吧?(可选)",widget=forms.RadioSelect,choices=Relationship.RANK_CHOICES,required=False)
    text = forms.CharField(label=u"简短附注",widget=forms.Textarea,required=False)

class PhotoForm(forms.Form):
    def __init__(self,place_set,*args,**kwargs):
        super(PhotoForm,self).__init__(*args,**kwargs)
        self.fields["place"] = forms.ModelChoiceField(label=u"拍摄地点",queryset=place_set)
    
    title = forms.CharField(label=u"标题")
    description = forms.CharField(label=u"描述",widget=forms.Textarea,required=False)
    image = forms.ImageField(label=u"图片路径")

class PlanForm(forms.Form):
    title = forms.CharField(label=u"旅程名称：")
    public = forms.BooleanField(label=u"是否公开",required=False,initial=True)

class PlayForm(forms.Form):
    begin_time = forms.DateTimeField(label=u"起始时间",widget=widgets.AdminSplitDateTime(attrs={'size': 20,}),required=False)
    end_time = forms.DateTimeField(label=u"结束时间",widget=widgets.AdminSplitDateTime(attrs={'size': 20,}),required=False)
    tips = forms.CharField(label=u"简短附注",widget=forms.Textarea,required=False)
    cost = forms.FloatField(label=u"预计花销",required=False)

class RouteForm(forms.Form):
    transportation = forms.ChoiceField(label=u"交通方式",widget=forms.RadioSelect,choices=Route.TRANS_CHOICES[:-1],initial=0)
    begin_time = forms.DateTimeField(label=u"起始时间",widget=widgets.AdminSplitDateTime(attrs={'size': 20,}),required=False)
    end_time = forms.DateTimeField(label=u"结束时间",widget=widgets.AdminSplitDateTime(attrs={'size': 20,}),required=False)
    tips = forms.CharField(label=u"简短附注",widget=forms.Textarea,required=False)
    cost = forms.FloatField(label=u"预计花销",required=False)