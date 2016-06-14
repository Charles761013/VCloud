from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from vod.models import Video


def index(request):
    video_list = Video.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['video_list'] = video_list

    return render(request, 'vod/index.html', context_dict)

@login_required
def personal_videos(request):
    current_user = request.user
    video_list = Video.objects.filter(user=current_user)

    context_dict = {}
    context_dict['video_list'] = video_list
    return render(request, 'vod/personal_videos.html', context_dict)

@login_required
def upload(request):
    context_dict = {}
    return render(request, 'vod/upload.html', context_dict)

def search(request):
    context_dict = {}
    if 'query' in request.GET:
        terms = request.GET['query']
        search_results = Video.objects.filter(Q(title__icontains=terms) |
                                        Q(user__username__icontains=terms)).order_by('-views')
        context_dict['search_results'] = search_results
        context_dict['do_search'] = True
    else:
        pass

    return render(request, 'vod/search.html', context_dict)


