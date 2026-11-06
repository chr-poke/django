from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cos", views.wip, name="cos"),
    path("produse", views.wip, name="produse"),
    path("istoric", views.wip, name="istoric"),
    path("intro", views.intro, name="intro"),
    path("contact", views.wip, name="contact"),
    path("info", views.info, name="info"),
    path("log", views.log, name="log"),
    re_path(r"^accesare(?P<id>\d+)/?$", views.accesare, name="accesare")
]
