from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny #どのviewでもアクセスできる
from . import serializers
from .models import Profile, Post, Comment


#setthings.pyでログインユーザー以外はViewにアクセスできないように設定している。
#しかし新規作成する画面だけはアクセスする必要があるためAllowAnyで上書きする。

#新規作成
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    #誰でもアクセス可能にする
    permission_classes = (AllowAny,)

#プロフィール新規作成・更新
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    #現在ログインしているユーザーをself.request.userで取得
    #perform_createをオーバーライド
    def perform_create(self, serializer):
        #userProfileはserializersで作ったもの
        serializer.save(userProfile=self.request.user)

#ログインしているユーザーのプロフィールを返す
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    #ユーザープロフィールとログインユーザーが一致しているオブジェクトをフィルター
    #get_querysetをオーバーライド
    def get_queryset(self):
        #userProfileはserializersで作ったもの
        return self.queryset.filter(userProfile=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    #現在ログインしているユーザーをself.request.userで取得
    #perform_createをオーバーライド
    def perform_create(self, serializer):
        #userPostはserializersで作ったもの
        serializer.save(userPost=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    #現在ログインしているユーザーをself.request.userで取得
    #perform_createをオーバーライド
    def perform_create(self, serializer):
        #userCommentはserializersで作ったもの
        serializer.save(userComment=self.request.user)
