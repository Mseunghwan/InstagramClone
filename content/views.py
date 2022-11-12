import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from Minstagram.settings import MEDIA_ROOT
from user.models import User
from .models import Feed, Reply, Like, Bookmark
#.은 현 폴더에서, models내 Feed 클래스를 사용한다는 것

class Main(APIView):
    def get(self, request):

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()  # 웹 서버 세션에 등록된 이메일 정보를 통해 유저 데이터 불러온다

        if user is None:
            return render(request, "user/login.html")

        feed_object_list = Feed.objects.all().order_by('-id') #feed_list에 Feed에 있는 모든 데이터를 가져오겠다는 것
        # 위 같이 Feed.objects.all()과 같은 라인이 쿼리셋 역할을 한다. 즉 sql쿼리 문에서 select * from content_feed와 같은 동작을 한다
        feed_list = []
        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_obejct_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_obejct_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    reply_content=reply.reply_content,
                    nickname=user.nickname
                )) # 댓글 목록들 추가

            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count() # like_count 역할을 해준다
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(
                            id=feed.id,
                            image=feed.image,
                            content=feed.content,
                            like_count=like_count,
                            profile_image=user.profile_image,
                            nickname=user.nickname,
                            reply_list=reply_list,
                            is_liked=is_liked,
                            is_marked=is_marked
                                  ))

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
        email = request.session.get('email', None)

        Feed.objects.create(image=image, content=content, email=email)

        return Response(status=200) #http response -- http:200(=success를 의미)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()  # 웹 서버 세션에 등록된 이메일 정보를 통해 유저 데이터 불러온다

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email).all()
        like_list = list(Like.objects.filter(email=email, is_like=True).all().values_list('feed_id', flat=True))
        # values_list 하면 속성명을 지정해서 해당 데이터만 가져올 수 있다 - query set으로 반환되는데 이를 list로 받아오기 위해서 list로 감싸주기
        like_feed_list = Feed.objects.filter(id__in=like_list)
        # id__in? 피드에 있는 아이디 중에 like_list 내에 있는 피드만 선택해서 가져올 수 있다
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).all().values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)


        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == "favorite_border":
            is_like = True
        else :
            is_like = False

        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()
        if like:
            like.is_like=is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)

        if bookmark_text == "bookmark_border":
            is_marked = True
        else:
            is_marked = False

        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)