from django.urls import path
from .views import Main, UploadFeed, Profile, UploadReply

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('profile', Profile.as_view()),
    path('main', Main.as_view())
]
