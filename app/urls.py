from dutyroster.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('addCand', views.addCand, name='addCand'),
    path('chngStatus', views.chngStatus, name='chngStatus'),
    path('tryit', views.tryit, name='tryit'),
    path('makeExcuse/', views.makeExcuse, name='makeExcuse'),
    path('messageNow', views.messageNow, name='messageNow'),
    path('eye3StartTask', views.eye3StartTask, name='eye3StartTask'),
    path('eye3DeleteTask', views.eye3DeleteTask, name='eye3DeleteTask')
]