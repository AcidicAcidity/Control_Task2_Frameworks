from django.urls import path
from . import views

app_name = "beauty"
urlpatterns = [
    path("", views.visit_list, name="visit_list"),
    path("statistics/", views.statistics, name="statistics"),          # ДО slug-маршрута!
    path("<slug:slug>/", views.visit_detail, name="visit_detail"),
]
