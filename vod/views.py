#coding:utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from vod.models import Video, Review, LikeVideo, LikeReview, ResponseReview
from django.db.models import F
from vod.forms import ReviewForm, UploadFileForm
from vod.fileutils import handle_uploaded_file, delete_uploaded_file, do_thumbnail, delete_thumbnail
import uuid, time, os

STREAMSERVER_HOST = "192.168.1.126"
STREAM_URL = "rtmp://" + STREAMSERVER_HOST + "/oflaDemo/{filename}"


def index(request):
    video_list = Video.objects.order_by('-views')
    context_dict = {}
    context_dict['video_list'] = video_list
    return render(request, 'vod/index.html', context_dict)

@login_required
def personal_videos(request):
    context_dict = {}
    if request.method == 'GET':
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            if not user_id or not user_id.isdigit():
                 return redirect('/vod/')
            user_id = int(user_id)
            personal_list = Video.objects.filter(user__id=user_id).order_by('-upload_date')
            context_dict['personal_list'] = personal_list
            get_like_list = LikeVideo.objects.filter(user__id=user_id)
            video_id_list = []
            for get_like in get_like_list:
                video_id_list.append(get_like.video.id)
            like_list = Video.objects.filter(id__in=video_id_list).order_by('-upload_date')
            context_dict['like_list'] = like_list

    return render(request, 'vod/personal_videos.html', context_dict)

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #print request.POST
        fileName = str(request.FILES['file'])
        if form.is_valid():
            #modify fileName to uuid, to prevent collision
            oldExt = fileName.split(".")[1]
            new_file_name = fileName + str(time.time())
            filename_uuid = str(uuid.uuid3(uuid.uuid1(), new_file_name))
            filename_uuid_new_ext = filename_uuid + ".mp4"
            filename_uuid_old_ext = filename_uuid + "." + oldExt

            handle_uploaded_file(request.FILES['file'], filename_uuid_old_ext)
            thumbnail_file = do_thumbnail(filename_uuid_old_ext)
            url = STREAM_URL.format(filename=filename_uuid_new_ext)
            new_video = Video.objects.create(user = request.user,
                                title = request.POST['title'],
                                description = request.POST['description'],
                                url = url,
                                thumbnail = thumbnail_file)
            form = UploadFileForm()
            #should sleep a while, to wait for video transcode
            return render(request, 'vod/upload.html', {'form': form, 'new_video': new_video})
    else:
        form = UploadFileForm()
    return render(request, 'vod/upload.html', {'form': form})

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

def videoplay(request):
    if request.method == 'GET':
        current_user = request.user
        if 'video_id' in request.GET:
            video_id = request.GET['video_id']
            if not video_id or not video_id.isdigit():
                 return redirect('/vod/')
            video_id = int(video_id)
            try:
                video = Video.objects.get(id=video_id)
            except Video.DoesNotExist:
                video = None
                return redirect('/vod/')
            if video:
                #F('views') + 1
                video.views = video.views + 1
                video.save()
                context_dict = {'video': video}
                reviews = Review.objects.filter(video=video).exclude(text=None)
                likes_number = LikeVideo.objects.filter(video=video).count()
                context_dict['reviews'] = reviews
                context_dict['likes_number'] = likes_number
                try:
                    isLike = LikeVideo.objects.get(video=video, user=current_user)
                except LikeVideo.DoesNotExist:
                    isLike = False
                context_dict['isLike'] = isLike
                form = ReviewForm()
                context_dict['form'] = form
                return render(request, 'vod/videoplay.html', context_dict)
            else:
                return redirect('/vod/')

        else:
             return redirect('/vod/')

    elif request.method == 'POST':
        video_id = request.POST['video_id']
        if not video_id or not video_id.isdigit():
            return redirect('/vod/')
        video_id = int(video_id)
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            video = None
            return redirect('/vod/')
        form = ReviewForm(request.POST)
        if form.is_valid():
            if video:
                review = form.save(commit=False)
                review.video = video
                review.user = request.user
                review.save()
        else:
            print form.errors
        return redirect('/vod/videoplay?video_id='+str(video_id))

@login_required
def like_video(request):
    video_id = None
    if request.method == 'GET':
        current_user = request.user
        video_id = request.GET['video_id']
        is_like = request.GET['is_like']
        video_id = int(video_id)
        is_like = int(is_like)
    likeNumber = 0
    if video_id and is_like:
        video = Video.objects.get(id=video_id)
        LikeVideo.objects.get_or_create(user=current_user, video=video, likes=True)
        likeNumber = LikeVideo.objects.filter(video__id=video_id).count()
        return HttpResponse(likeNumber)
    elif video_id and not is_like:
        LikeVideo.objects.get(user=current_user, video__id=video_id).delete()
        likeNumber = LikeVideo.objects.filter(video__id=video_id).count()
        return HttpResponse(likeNumber)
    else:
        return HttpResponseNotFound()

@login_required
def review(request):
    if request.method == 'GET': #delete
        review_id = request.GET['review_id']
        review_id = int(review_id)
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return redirect('/vod/')
        review.delete()
        return HttpResponse("<h4>delete success!<h4>")
    elif request.method == 'POST': #edit
        review_id = request.POST['review_id']
        review_id = int(review_id)
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return redirect('/vod/')
        if review:
            text = request.POST['content']
            review.text = text
            review.save()
            return HttpResponse(text)
    else:
        return redirect('/vod/')

@login_required
def delete_video(request):
    if request.method == 'GET': #delete
        video_id = request.GET['video_id']
        video_id = int(video_id)
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return HttpResponse("no this video!")
        video.delete()
        #delete the video file
        filename = video.url.split("/")[-1]
        delete_uploaded_file(filename)
        delete_thumbnail(filename)
        return HttpResponse("delete success!")
    else:
        return redirect('/vod/')

'''
@login_required
def add_review(request):
    if request.method == 'POST':
        video_id = request.POST['video_id']
        if not video_id or not video_id.isdigit():
            return redirect('/vod/')
        video_id = int(video_id)
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            video = None
            return redirect('/vod/')
        form = ReviewForm(request.POST)
        if form.is_valid():
            if video:
                review = form.save(commit=False)
                review.video = video
                review.user = request.user
                review.save()

        else:
            print form.errors
    else:
        form = ReviewForm()
    context_dict = {'form': form}
    return render(request, 'vod/add_review.html', context_dict)
'''




