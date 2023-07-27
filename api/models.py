from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

#アバター画像アップロード先取得
def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])

#投稿画像アップロード先取得
def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])

#Email認証にするためにUserManagerをオーバーライド
class UserManager(BaseUserManager):

    #一般ユーザー
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')
        #Email正規化
        user = self.model(email=self.normalize_email(email))
        #passwordハッシュ化
        user.set_password(password)
        user.save(using=self._db)
        return user

    #スーパーユーザー
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        #ユーザーが有効か無効か
        user.is_active = True
        #Adminの画面にログインできる
        user.is_staff = True
        #Adminの画面にログインできるだけでなくデータの編集も可能。
        user.is_superuser = True
        user.save(using= self._db)

        return user

#Email認証できるようオーバーライド
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    #ユーザーそのものが有効か無効か
    is_active = models.BooleanField(default=True)
    #Adminにログインする権限
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName

class Post(models.Model):
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked',blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text