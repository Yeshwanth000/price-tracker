from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('price/',views.index,name='index'),
    path('about/',views.about,name='about'),
]