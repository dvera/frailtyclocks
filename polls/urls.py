from django.urls import path
from . import test
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name="test"),
    path('upload', views.upload, name='upload'),
    path('graphdata',views.graphdata,name='graphdata'),
]
