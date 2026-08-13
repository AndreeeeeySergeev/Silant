from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Клиент"
        SERVICE = "service", "Сервисная организация"
        MANAGER = "manager", "Менеджер"

    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )
    company_name = models.CharField(max_length=255, blank=True)
    company_description = models.TextField(blank=True)


class Directory(models.Model):
    class Entity(models.TextChoices):
        MACHINE_MODEL = "machine_model", "Модель техники"
        ENGINE_MODEL = "engine_model", "Модель двигателя"
        TRANSMISSION_MODEL = "transmission_model", "Модель трансмиссии"
        DRIVE_AXLE_MODEL = "drive_axle_model", "Модель ведущего моста"
        STEERING_AXLE_MODEL = "steering_axle_model", "Модель управляемого моста"
        MAINTENANCE_TYPE = "maintenance_type", "Вид ТО"
        FAILURE_NODE = "failure_node", "Узел отказа"
        RECOVERY_METHOD = "recovery_method", "Способ восстановления"

    entity = models.CharField(max_length=30, choices=Entity.choices)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_entity_display()}: {self.name}"

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    machine_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="machine_models",)
    engine_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="engine_models")
    engine_serial_number = models.CharField(max_length=255)
    transmission_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="transmission_models")
    transmission_serial_number = models.CharField(max_length=255)
    drive_axle_model = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                         related_name="drive_axle_models")
    drive_axle_serial_number = models.CharField(max_length=255)
    steering_axle_model = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                            related_name="steering_axle_models")
    steering_axle_serial_number = models.CharField(max_length=255)
    supply_contract = models.CharField(max_length=100)
    shipment_date = models.DateField()
    consignee = models.CharField(max_length=100)
    operation_address = models.CharField(max_length=300)
    equipment = models.TextField(blank=True)
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="machines_as_client")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                        related_name="machines_as_service_company")

    def clean(self):
        super().clean()

        if self.machine_model.entity != Directory.Entity.MACHINE_MODEL:
            raise ValidationError ("В поле 'Модель техники' должна быть выбрана модель техники")

        if self.engine_model.entity != Directory.Entity.ENGINE_MODEL:
            raise ValidationError("В поле 'Модель двигателя' должна быть выбрана модель двигателя")

        if self.transmission_model.entity != Directory.Entity.TRANSMISSION_MODEL:
            raise ValidationError("В поле 'Модель трансмиссии' должна быть выбрана модель трансмиссии")

        if self.drive_axle_model.entity != Directory.Entity.DRIVE_AXLE_MODEL:
            raise ValidationError("В поле 'Модель ведущего моста' должна быть выбрана модель ведущео моста")

        if self.steering_axle_model.entity != Directory.Entity.STEERING_AXLE_MODEL:
            raise ValidationError(
                "В поле 'Модель управляемого моста' должна быть выбрана модель уаправляемого моста"
            )

        if self.client.role != User.Role.CLIENT:
            raise ValidationError("В поле 'Клиент' должен быть выбран пользователь с ролью 'Клиент'")

        if self.service_company.role != User.Role.SERVICE:
            raise ValidationError(
                "В поле 'Сервисная компания' должен быть выбран пользователь с ролью 'Сервисная организация'"
            )

class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                         related_name="maintenances_by_type")
    maintenance_date = models.DateField()
    operating_hours = models.PositiveIntegerField()
    work_order_number = models.CharField(max_length=100)
    work_order_date = models.DateField()
    maintenance_organization = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                                 related_name="maintenances_by_organization")
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT,
                                related_name="maintenances")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                        related_name="maintenances_as_service_company")