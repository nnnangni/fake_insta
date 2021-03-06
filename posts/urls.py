from django.urls import path
from . import views

app_name = 'posts'

# id가 있는 애들은 그 아이디에만 적용, 없으면 전체 적용
urlpatterns = [
    path('', views.list, name='list'),
    path('create/',views.create, name='create'),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),
    
    path('<int:post_id>/comment/create/', views.comment_create, name="comment_create"),
    # path('<int:post_id>/comment/delete/', views.comment_delete, name="comment_delete"),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name="comment_delete"),
    
    # 왜 create 안하나요? 
    path('<int:id>/like/', views.like, name="like"),
]