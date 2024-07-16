from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('user_update', views.user_update, name='user_update'),
    path('update_profile_image', views.update_profile_image, name='update_profile_image'),
    path('tweet_like/<int:pk>/', views.tweet_like, name='tweet_like'),
    path('tweet_delete/<int:pk>/', views.tweet_delete, name='tweet_delete'),
]
