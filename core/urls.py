from django.urls import path
from . import views
from .views import UserLoginView, UserLogoutView

app_name = "core"

urlpatterns = [
    path("machines/", views.machine_list, name="machine_list"),
    path("machines/<int:pk>/", views.machine_detail, name="machine_detail"),
    path("machines/create/", views.machine_create, name="machine_create"),
    path("maintenance/<int:pk>/", views.maintenance_detail, name="maintenance_detail"),
    path("maintenance/create/", views.maintenance_create, name="maintenance_create"),
    path("claims/", views.claim_list, name="claim_list"),
    path("claims/<int:pk>/", views.claim_detail, name="claim_detail"),
    path("claims/create/", views.claim_create, name="claim_create"),
    path("search/", views.guest_machine_search, name="guest_machine_search"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout")
]