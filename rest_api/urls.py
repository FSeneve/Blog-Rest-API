from django.urls import path, include
from .views import PostsView, post_detail,PostsAPIView,postDetailsAPIView, genericApiView, PostViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
      # path('posts/', PostsView),
      # path('details/<int:id>/', post_detail),
      
#      path('posts/', PostsAPIView.as_view()),
#      path('details/<int:id>/', postDetailsAPIView.as_view()),
       path('genericApiView/<int:id>/', genericApiView.as_view()),
       path('', include(router.urls)),
]