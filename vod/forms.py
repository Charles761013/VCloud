#coding:utf-8
from django import forms
from django.contrib.auth.models import User
from vod.models import Review, ResponseReview

class ReviewForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '留言'}))

  class Meta:
    model = Review
    fields = ['text']
