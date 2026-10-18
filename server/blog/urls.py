from django.urls import path
from . import views

from django.urls import include
from rest_framework import routers


router = routers.DefaultRouter()
router.register('Posts', views.IntruderImage)

urlpatterns=[
    path('api_root/', include(router.urls), name='api_root'),
    path('api_root/latest-UCF/', views.LatestUCFPostView.as_view(), name='latest-UCF'), 
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
]