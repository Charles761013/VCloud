from django.contrib import admin
from vod.models import Video, Review, LikeReview

admin.site.register(Video)
admin.site.register(Review)
admin.site.register(LikeReview)
