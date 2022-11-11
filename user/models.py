from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    """
        유저 프로필 사진
        유저 닉네임      -> 화면에 표기되는 이름
        유저 이름       -> 실제 사용자 이름
        유저 이메일 주소  -> 회원 가입시 사용하는 아이디
        유저 비밀번호    -> 장고에서 제공하는 디폴트 사용
    """
    profile_image = models.TextField()
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'nickname'
    """
       만약에 테이블 명을 안정하면 user(앱이름)_User(클래스명) 이런 식으로 생성될 것이다
       Meta 클래스를 통해 db_table의 이름을 설정할 수 있다
       """
    class Meta:
        db_table = "User"
