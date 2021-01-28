from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name ='home'),
    path('postlist/',views.ProfileListView, name='postlist'),
    path('create/',views.CreatePost.as_view(),name='createpost'),
    path('visualization/',views.Visualization, name='visual'),

]