import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Minstagram.settings import MEDIA_ROOT
from user.models import User
from .models import Feed
#.은 현 폴더에서, models내 Feed 클래스를 사용한다는 것

class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') #feed_list에 Feed에 있는 모든 데이터를 가져오겠다는 것
        # 위 같이 Feed.objects.all()과 같은 라인이 쿼리셋 역할을 한다. 즉 sql쿼리 문에서 select * from content_feed와 같은 동작을 한다

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first() # 웹 서버 세션에 등록된 이메일 정보를 통해 유저 데이터 불러온다

        if user is None:
            return render(request, "user/login.html")

        return render(request, "minstagram/main.html", context=dict(feeds=feed_list, user=user)) # 딕셔너리 형태로 feed_list 데이터를 넘겨주기


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        uuid_name = uuid4().hex # 이미지에 고유한 id부여를 위해 랜덤하게 글자를 정함
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, "wb+") as destination: # with open~ 부분이 실제로 파일을 저장하는 부분, save_path에 파일을 열어 조각조각 가져와 쓴다 - 그냥 알고만 있기
            for chunk in file.chunks(): # 파일변수명.chunks로 가져올 수 있다잉
                destination.write(chunk)
        # 이렇게 저장된 경로를 담아주기 - 이미지에
        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200) #http response -- http:200(=success를 의미)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()  # 웹 서버 세션에 등록된 이메일 정보를 통해 유저 데이터 불러온다

        if user is None:
            return render(request, "user/login.html")

        return render(request, 'content/profile.html', context=dict(user=user))