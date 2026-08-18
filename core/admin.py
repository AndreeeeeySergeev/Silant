from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import *

from .forms import (
    MachineForm,
    MaintenanceForm,
    ClaimForm,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "role",
        "company_name",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "company_name",
    )

    # Форма редактирования существующего пользователя
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "role",
                    "company_name",
                    "company_description",
                )
            },
        ),
    )

    # Форма создания нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                )
            },
        ),
        (
            "Персональные данные",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": (
                    "role",
                    "company_name",
                    "company_description",
                )
            },
        ),
    )


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "entity",
        "description",
    )

    list_filter = (
        "entity",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm

    list_display = (
        "serial_number",
        "machine_model",
        "engine_model",
        "client",
        "service_company",
        "shipment_date",
    )

    list_filter = (
        "machine_model",
        "engine_model",
        "client",
        "service_company",
    )

    search_fields = (
        "serial_number",
        "engine_serial_number",
        "transmission_serial_number",
        "drive_axle_serial_number",
        "steering_axle_serial_number",
    )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceForm

    list_display = (
        "maintenance_date",
        "maintenance_type",
        "machine",
        "maintenance_organization",
        "service_company",
        "operating_hours",
    )

    list_filter = (
        "maintenance_type",
        "service_company",
    )

    search_fields = (
        "work_order_number",
        "machine__serial_number",
    )


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    form = ClaimForm

    list_display = (
        "failure_date",
        "machine",
        "failure_node",
        "recovery_method",
        "recovery_date",
        "service_company",
        "display_downtime",
    )

    list_filter = (
        "failure_node",
        "recovery_method",
        "service_company",
    )

    search_fields = (
        "machine__serial_number",
        "failure_description",
    )

    @admin.display(description="Время простоя техники, дней")
    def display_downtime(self, obj):
        return obj.downtime