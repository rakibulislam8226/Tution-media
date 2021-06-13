
from django.urls import path, include
from . import views




urlpatterns = [
  path('', views.home, name='home'),
  path('search/', views.search, name='search'),
  path('about_us/', views.about_us, name='about_us'),
  path('feedback/', views.feedback, name='feedback'),
  path('contact/', views.contact, name='contact'),
  path('createpost/', views.createpost, name='createpost'),
  # path('createpost/', views.PostCreateView.as_view(), name='createpost'),
  path('postlist/', views.PostListView.as_view(), name='postlist'),
  # path('postlist/', views.postlist, name='postlist'),
  path('likepost/<int:id>/', views.likepost, name='likepost'),
  path('addcomment/', views.addcomment, name='addcomment'),
  path('deletecomment/<int:id>/', views.deletecomment, name='deletecomment'),
  path('postdetail/<int:pk>/', views.PostDetailView.as_view(), name='postdetail'),
  path('postedit/<int:pk>/', views.PostEditView.as_view(), name='postedit'),
  path('postdelete/<int:pk>/', views.PostDeleteView.as_view(), name='postdelete'),
  path('userprofile/', include('userprofile.urls')),
  path('notification/', views.notification, name='notification'),
]

