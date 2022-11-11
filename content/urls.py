from django.urls import path
from .views import Main, UploadFeed, Profile

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('profile', Profile.as_view()),
    path('main', Main.as_view())
]
