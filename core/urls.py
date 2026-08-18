from django.urls import path
from . import views
from .views import UserLoginView, UserLogoutView

app_name = "core"

urlpatterns = [
    path("machines/", views.machine_list, name="machine_list"),
    path("machines/create/", views.machine_create, name="machine_create"),
    path("machines/<int:pk>/", views.machine_detail, name="machine_detail"),
    path("maintenance/", views.maintenance_list, name="maintenance_list"),
    path("maintenance/create/", views.maintenance_create, name="maintenance_create"),
    path("maintenance/<int:pk>/", views.maintenance_detail, name="maintenance_detail"),
    path("claims/", views.claim_list, name="claim_list"),
    path("claims/create/", views.claim_create, name="claim_create"),
    path("claims/<int:pk>/", views.claim_detail, name="claim_detail"),
    path("search/", views.guest_machine_search, name="guest_machine_search"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout")
]