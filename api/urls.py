from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

#routerが使用できるのは「ModelViewSet」を継承しているView
#pathとviewをrouterで紐づけする
router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)

#汎用viewで作ったviewは下記の書き方で紐づけ
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('',include(router.urls))
]