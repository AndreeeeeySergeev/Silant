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
        choices=Role.choices,
        verbose_name="Роль",
    )
    company_name = models.CharField(max_length=255, blank=True, verbose_name="Название компании")
    company_description = models.TextField(blank=True, verbose_name="Описание компании")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


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
        MAINTENANCE_ORGANIZATION = "maintenance_organization", "Организация, проводившая ТО"

    entity = models.CharField(max_length=30, choices=Entity.choices, verbose_name="Тип справочника")
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Запись справочника"
        verbose_name_plural = "Справочник"

    def __str__(self):
        return f"{self.get_entity_display()}: {self.name}"

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True, verbose_name="Зав. № машины")
    machine_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="machine_models",
                                      verbose_name="Модель техники",)
    engine_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="engine_models",
                                     verbose_name="Модель двигателя",)
    engine_serial_number = models.CharField(max_length=255, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name="transmission_models",
                                           verbose_name="Модель трансмиссии")
    transmission_serial_number = models.CharField(max_length=255, verbose_name="Зав. № трансмиссии")
    drive_axle_model = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                         related_name="drive_axle_models", verbose_name="Модел ведущего моста")
    drive_axle_serial_number = models.CharField(max_length=255, verbose_name="Зав. № ведущего моста")
    steering_axle_model = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                            related_name="steering_axle_models",
                                            verbose_name="Модель управляемого моста",)
    steering_axle_serial_number = models.CharField(max_length=255, verbose_name="Зав. № управляемого моста")
    supply_contract = models.CharField(max_length=100, verbose_name="Договор поставки №, дата")
    shipment_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=100, verbose_name="Грузополучатель (конечный потребитель)")
    operation_address = models.CharField(max_length=300, verbose_name="Адрес поставки (эксплуатации)")
    equipment = models.TextField(blank=True, verbose_name="Комплектация (доп. опции)")
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="machines_as_client", verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                        related_name="machines_as_service_company", verbose_name="Сервисная компания")
    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self):
        return self.serial_number

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
                                         related_name="maintenances_by_type", verbose_name="Вид ТО",)
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    operating_hours = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    work_order_number = models.CharField(max_length=100, verbose_name="№ заказ-наряда")
    work_order_date = models.DateField(verbose_name="Дата заказ-наряда")
    maintenance_organization = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                                 related_name="maintenances_by_organization",
                                                 verbose_name="Организация, проводившая ТО",)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT,
                                related_name="maintenances", verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                        related_name="maintenances_as_service_company",
                                        verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Техническое обслуживание"

    def clean(self):
        super().clean()

        if self.maintenance_type.entity != Directory.Entity.MAINTENANCE_TYPE:
            raise ValidationError("В поле 'Вид ТО' должна быть выбрана запись из"
                                  "справочника 'Вид ТО'")

        if self.maintenance_organization.entity != Directory.Entity.MAINTENANCE_ORGANIZATION:
            raise ValidationError("В поле 'Организация, проводившая ТО' должна быть выбрана "
            "организация из справочника 'Организация, проводившая ТО'")

        if self.service_company.role != User.Role.SERVICE:
            raise ValidationError(
                "В поле 'Сервисная компания' должен быть выбран пользователь "
                "с ролью 'Сервисная организация'"
            )

class Claim(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_hours = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                     related_name="claims_by_failure_node", verbose_name="Узел отказа",)
    failure_description = models.TextField(verbose_name="Описание отказа",)
    recovery_method = models.ForeignKey(Directory, on_delete=models.PROTECT,
                                        related_name="claims_by_recovery_method", verbose_name="Способ восстановления",)
    spare_parts = models.TextField(blank=True, verbose_name="Используемые запасные части") # если ремонт проводился без замены деталей
    recovery_date = models.DateField(null=True, blank=True, verbose_name="Дата восстановления") # если реионт ещё не проводился, то разрешаем быть пустым
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name="claims", verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                        related_name="claims_as_service_company", verbose_name="Сервисная компания",)

    # вычисляем 8 поле Время простоя техники
    @property
    def downtime(self):
        if self.recovery_date and self.failure_date:
            return (self.recovery_date - self.failure_date).days
        return None

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"

    def clean(self):
        super().clean()

        if self.failure_node.entity !=Directory.Entity.FAILURE_NODE:
            raise ValidationError(
                "В поле 'Узел отказа' должна быть выбрана запись из справочника 'Узел отказа'"
            )
        if self.recovery_method.entity != Directory.Entity.RECOVERY_METHOD:
            raise ValidationError(
                "В поле 'Способ восстановления' должна быть выбрана"
                " запись из справочника 'Способ восстановления'"
            )
        if self.service_company.role != User.Role.SERVICE:
            raise ValidationError(
                "В поле 'Сервисная компания' должен быть выбран пользователь"
                "с ролью 'Сервисная организация'"
            )
        if self.recovery_date and self.recovery_date < self.failure_date:
            raise ValidationError(
                "Дата восстановления не может быть раньше даты отказа"
            )