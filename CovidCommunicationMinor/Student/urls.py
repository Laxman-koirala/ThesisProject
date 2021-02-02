from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name ='home'),
    path('postlist/',views.ProfileListView, name='postlist'),
    path('create/',views.CreatePost.as_view(),name='createpost'),
    path('users/', views.ProfileList.as_view(), name='users'),
    path('visualization/',views.Visualization, name='visual'),
    path('<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/', views.Myprofile, name='profile'),
    path('search/', views.search, name='search'),

]