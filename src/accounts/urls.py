from django.urls import path

from .views import ProfileDetailView

urlpatterns = [
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
]
