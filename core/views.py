from allauth.socialaccount.sessions import engine
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def machine_list(request):
    user = request.user

    # доступ к машинам по ролям
    if user.role == user.Role.MANAGER:
        machines = Machine.objects.all()

    elif user.role == user.Role.CLIENT:
        machines = Machine.objects.filter(client=user)

    elif user.role == user.Role.SERVICE:
        machines = Machine.objects.filter(service_company=user)

    else:
        machines = Machine.objects.none()

    machine_model = request.GET.get("machine_model")

    if machine_model:
        machines = machines.filter(
            machine_model_id=machine_model
        )

    engine_model = request.GET.get("engine_model")

    if engine_model:
        machines = machines.filter(
            engine_model_id = engine_model
        )

    transmission_model = request.GET.get("transmission_model")

    if transmission_model:
        machines = machines.filter(
            transmission_model_id = transmission_model
        )

    steering_axle_model = request.GET.get("steering_axle_model")

    if steering_axle_model:
        machines = machines.filter(
            steering_axle_model_id = steering_axle_model
        )

    drive_axle_model = request.GET.get("drive_axle_model")

    if drive_axle_model:
        machines = machines.filter(
            drive_axle_model_id = drive_axle_model
        )

    sort = request.GET.get("sort", "shipment_date")

    allowed_sort_fields = {
        "shipment_date",
        "-shipment_date",
        "serial_number",
        "-serial_number",
    }

    if sort not in allowed_sort_fields:
        sort = "shipment_date"

    machines =  machines.order_by(sort)

    machine_models = Directory.objects.filter(
        entity = Directory.Entity.MACHINE_MODEL
    )

    engine_models = Directory.objects.filter(
        entity = Directory.Entity.ENGINE_MODEL
    )

    transmission_models = Directory.objects.filter(
        entity = Directory.Entity.TRANSMISSION_MODEL
    )

    steering_axle_models = Directory.objects.filter(
        entity = Directory.Entity.STEERING_AXLE_MODEL
    )

    drive_axle_models = Directory.objects.filter(
        entity = Directory.Entity.DRIVE_AXLE_MODEL
    )

    context = {
        "machines": machines,

        "machine_models": machine_models,
        "engine_models": engine_models,
        "transmission_models": transmission_models,
        "steering_axle_models": steering_axle_models,
        "drive_axle_models": drive_axle_models,

        "current_sort": sort,
    }

    return render(
        request,
        "core/machine_list.html",
        context
    )