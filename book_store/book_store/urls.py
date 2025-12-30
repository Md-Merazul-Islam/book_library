from django.urls import path, include, re_path
from django.http import HttpResponse
from django.contrib import admin


def favicon(request):
    return HttpResponse(status=204)
def home(request):
    return HttpResponse("Welcome to the Book Store API")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    re_path(r"^favicon.ico$", favicon),
    path(
        "api/v1/",
        include(
            [
                path("library/", include("library.urls")),
            ]
        ),
    ),
]
