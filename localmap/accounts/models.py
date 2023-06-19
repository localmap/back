from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

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