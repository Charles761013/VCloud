from django.contrib import admin
from vod.models import Video, Review, LikeReview, LikeVideo, ResponseReview

admin.site.register(Video)
admin.site.register(Review)
admin.site.register(LikeVideo)
admin.site.register(ResponseReview)
admin.site.register(LikeReview)

