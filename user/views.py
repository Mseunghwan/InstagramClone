import os
from uuid import uuid4
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from Minstagram.settings import MEDIA_ROOT
from .models import User

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            # (아래)패스워드 생성 - 암호화
                            password = make_password(password),
                            profile_image="default_profile.jpeg")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()
        # first()를 쓰는 이유? 쓰지 않으면 list형식으로 불러와지는데 first를 쓰면 첫 번째 값만 가져올 수 있기에 바로 가능
        if user is None:
            return Response(status=400, data=dict(message='회원정보가 잘못되었습니다'))

        print(user.check_password(password))
        if user.check_password(password):
            # TODO 로그인을 했다. 세션 혹은 쿠키에 넣는다.
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message='회원정보가 잘못되었습니다'))

class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')

class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')
        uuid_name = uuid4().hex # 이미지에 고유한 id부여를 위해 랜덤하게 글자를 정함
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, "wb+") as destination: # with open~ 부분이 실제로 파일을 저장하는 부분, save_path에 파일을 열어 조각조각 가져와 쓴다 - 그냥 알고만 있기
            for chunk in file.chunks(): # 파일변수명.chunks로 가져올 수 있다잉
                destination.write(chunk)
        # 이렇게 저장된 경로를 담아주기 - 이미지에
        profile_image = uuid_name

        user = User.objects.filter(email=email).first()
        user.profile_image = profile_image
        user.save() # create일 때는 안해두 되지만 객체를 불러와서 수정과정을 거친 후에는 save()를 해주어야 한다

        return Response(status=200) #http response -- http:200(=success를 의미)