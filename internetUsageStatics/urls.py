from django.urls import path

from . import views

urlpatterns = [
    path("data_usage", views.DataUsageDetails.as_view(), name="upload_csv"),
]