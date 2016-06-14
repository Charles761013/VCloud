from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def index(request):
	context_dict = {}
	return render(request, 'vod/index.html', context_dict)

def personal_videos(request):
	context_dict = {}
	return render(request, 'vod/personal_videos.html', context_dict)
