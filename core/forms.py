from django import forms
from .models import Machine, Directory, User, Maintenance, Claim

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "company_name",
            "company_description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если создаём нового пользователя,
        # поля компании пока скрываем
        if self.instance.role != User.Role.SERVICE:
            self.fields["company_name"].widget = forms.HiddenInput()
            self.fields["company_description"].widget = forms.HiddenInput()

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["machine_model"].queryset = Directory.objects.filter(
                entity=Directory.Entity.MACHINE_MODEL
            )

            self.fields["engine_model"].queryset = Directory.objects.filter(
                entity=Directory.Entity.ENGINE_MODEL
            )

            self.fields["transmission_model"].queryset = Directory.objects.filter(
                entity=Directory.Entity.TRANSMISSION_MODEL
            )

            self.fields["drive_axle_model"].queryset = Directory.objects.filter(
                entity=Directory.Entity.DRIVE_AXLE_MODEL
            )

            self.fields["steering_axle_model"].queryset = Directory.objects.filter(
                entity=Directory.Entity.STEERING_AXLE_MODEL
            )

            self.fields["client"].queryset = User.objects.filter(
                role = User.Role.CLIENT,
                is_active = True,
            )

            self.fields["service_company"].queryset = User.objects.filter(
                role = User.Role.SERVICE,
                is_active = True,
            )

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["maintenance_type"].queryset = Directory.objects.filter(
            entity=Directory.Entity.MAINTENANCE_TYPE
        )

        self.fields["maintenance_organization"].queryset = Directory.objects.filter(
            entity=Directory.Entity.MAINTENANCE_ORGANIZATION
        )

        self.fields["machine"].queryset = Machine.objects.all()

        self.fields["service_company"].queryset = User.objects.filter(
            role=User.Role.SERVICE,
            is_active=True,
        )

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["failure_node"].queryset = Directory.objects.filter(
            entity=Directory.Entity.FAILURE_NODE
        )

        self.fields["recovery_method"].queryset = Directory.objects.filter(
            entity=Directory.Entity.RECOVERY_METHOD
        )

        self.fields["machine"].queryset = Machine.objects.all()

        self.fields["service_company"].queryset = User.objects.filter(
            role=User.Role.SERVICE,
            is_active=True,
        )