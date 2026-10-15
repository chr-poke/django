from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("info", views.info, name="info"),
    path("log", views.log, name="log"),
    path("istoric", views.istoric, name="istoric"),
    path("despre", views.despre, name="despre"),
    re_path(r"^accesare(?P<id>\d+)/?$", views.accesare, name="accesare")
]
