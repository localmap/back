from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from hjd.models import Hjd
#헬퍼 class
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

# 실제 class
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True,
    )
    name = models.CharField(max_length=30, unique=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    location = models.ForeignKey(Hjd, on_delete=models.PROTECT, null=True, db_column='location', to_field='adm_nm')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
# 권한알림
    def has_perm(self, perm, obj=None):
        return True
# App Model 접근 가능
    def has_module_perms(self, app_label):
        return True
# 장고 관리자 화면 로그인
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'user'  # 테이블명을 user로 설정

    # 비밀번호 재설정 메소드
    def set_new_password(self, new_pw):
        # 여기에서 비밀번호 재설정 로직을 구현합니다.
        # 예를 들어, 입력된 새 비밀번호를 해싱하여 저장할 수 있습니다.
        hashed_pw = make_password(new_pw)
        self.password = hashed_pw
        self.save()

    def confirm_password(self, pw_confirm):
        # 여기에서 비밀번호 확인 로직을 구현합니다.
        # 예를 들어, 입력된 비밀번호와 저장된 해싱된 비밀번호를 비교할 수 있습니다.
        return check_password(pw_confirm, self.password)