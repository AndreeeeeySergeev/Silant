from django import forms
from .models import Machine, Directory, User, Maintenance, Claim


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

        self.fields["service_company"].queryset = User.objects.filter(
            role=User.Role.SERVICE,
            is_active=True,
        )

        if user is None:
            self.fields["machine"].queryset = Machine.objects.none()

        elif user.role == User.Role.MANAGER:
            self.fields["machine"].queryset = Machine.objects.all()
            self.fields["service_company"].queryset = User.objects.filter(
                role = User.Role.SERVICE,
                is_active = True
            )

        elif user.role == User.Role.CLIENT:
            self.fields["machine"].queryset = Machine.objects.filter(
                client=user
            )

        elif user.role == User.Role.SERVICE:
            self.fields["machine"].queryset = Machine.objects.filter(
                service_company=user
            )

            self.fields["service_company"].queryset = User.objects.filter(
                pk = user.pk
            )

        else:
            self.fields["machine"].queryset = Machine.objects.none()


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

        self.fields["service_company"].queryset = User.objects.filter(
            role=User.Role.SERVICE,
            is_active=True,
        )

        if user is None:
            self.fields["machine"].queryset = Machine.objects.none()


        elif user.role == User.Role.MANAGER:
            self.fields["machine"].queryset = Machine.objects.all()
            self.fields["service_company"].queryset = User.objects.filter(
                role=User.Role.SERVICE,
                is_active=True,
            )


        elif user.role == User.Role.SERVICE:
            self.fields["machine"].queryset = Machine.objects.filter(
                service_company=user
            )
            self.fields["service_company"].queryset = User.objects.filter(
                pk=user.pk
            )

        else:
            self.fields["machine"].queryset = Machine.objects.none()