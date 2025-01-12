from django.urls import path
from . import views


urlpatterns = [
    path('', views.LogIn, name='LogIn'),
    path('register/', views.Register, name='Register'),
    path('blogs/',views.Blogs,name='Blogs'),
    path('create/', views.CreateBlog, name='CreateBlog'),  # Form to create a blog
    path('blogs/<slug:slug>/', views.BlogDetail, name='BlogDetail'),
    path('Authorlogs/<int:blog_id>/', views.Authorlogs, name='Authorlogs'),
    path('MyBlogs/<str:user_email>/', views.MyBlogs, name='MyBlogs'),
    path('EditBlog/<int:blog_id>/', views.EditBlog, name='EditBlog'),
    path('blog/<int:blog_id>/like/', views.LikeBlog, name='LikeBlog'),
    path('blog/<int:blog_id>/unlike/', views.UnLikeBlog, name='UnLikeBlog'),
]
