from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('register',views.register),
    path('success',views.success),
    path('logout',views.logout),
    path('addwish',views.addwish),
    path('grant/<int:id>',views.grant),
    path('delete/<int:id>',views.delete),
    path('edit/<int:id>',views.edit),
    path('liked/<int:id>',views.like),
    path('stats',views.stats)
]