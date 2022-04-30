from django.urls import path

from .views import ListNewCheckAPIView, CreateChecksAPIView, get_check_pdf

urlpatterns = [
    path(
        "new_checks/",
        ListNewCheckAPIView.as_view(),
        name="new_checks",
    ),
    path(
        "create_checks/",
        CreateChecksAPIView.as_view(),
        name="create_checks",
    ),
    path("check/", get_check_pdf),
]
