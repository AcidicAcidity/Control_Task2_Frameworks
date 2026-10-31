from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("cabinets/", include("cabinets.urls")),
    path("beauty/", include("beauty.urls")),
]
