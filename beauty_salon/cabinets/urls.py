from django.urls import path
from . import views

app_name = "cabinets"
urlpatterns = [path("", views.cabinet_list, name="cabinet_list")]
