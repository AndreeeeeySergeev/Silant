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

@login_required
def maintenance_list(request):
    user = request.user

    if user.role == user.Role.MANAGER:
        maintenances = Maintenance.objects.all()

    elif user.role == user.Role.CLIENT:
        maintenances = Maintenance.objects.filter(
            machine__client = user
        )

    elif user.role == user.Role.SERVICE:
        maintenances = Maintenance.objects.filter(
            service_company = user
        )

    else:
        maintenances = Maintenance.objects.none()

    maintenance_type = request.GET.get("maintenance_type")

    if maintenance_type:
        maintenances = maintenances.filter(
            maintenance_type_id = maintenance_type
        )

    machine = request.GET.get("machine")

    if machine:
        maintenances = maintenances.filter(
            machine_id = machine
        )

    service_company = request.GET.get("service_company")

    if service_company:
        maintenances = maintenances.filter(
            service_company_id = service_company
        )

    sort = request.GET.get("sort", "maintenance_date")

    allowed_sort_fields = {
        "maintenance_date",
        "-maintenance_date",
    }

    if sort not in allowed_sort_fields:
        sort = "maintenance_date"

    maintenances = maintenances.order_by(sort)

    maintenance_types = Directory.objects.filter(
        entity = Directory.Entity.MAINTENANCE_TYPE
    )

    if user.role == User.Role.MANAGER:
        machines = Machine.objects.all()

    elif user.role == User.Role.CLIENT:
        machines = Machine.objects.filter(
           client = user
        )

    elif user.role == User.Role.SERVICE:
        machines = Machine.objects.filter(
            service_company = user
        )
    else:
        machines = Machine.objects.none()

    service_companies = User.objects.filter(
        role = User.Role.SERVICE,
        is_active = True,
    )

    context = {
        "maintenances": maintenances,
        "maintenance_types": maintenance_types,
        "machines": machines,
        "service_companies": service_companies,
    }


    return render (
        request,
        "core/maintenance_list.html",
        context,
    )

@login_required
def claim_list(request):
    user = request.user

    if user.role == User.Role.MANAGER:
        claims = Claim.objects.all()

    elif user.role == User.Role.CLIENT:
        claims = Claim.objects.filter(
            machine__client = user
        )

    elif user.role == User.Role.SERVICE:
        claims = Claim.objects.filter(
            service_company = user
        )
    else:
        claims = Claim.objects.none()

    failure_node = request.GET.get("failure_node")

    if failure_node:
        claims = claims.filter(
            failure_node_id = failure_node
        )

    recovery_method = request.GET.get("recovery_method")

    if recovery_method:
        claims = claims.filter(
            recovery_method_id = recovery_method
        )

    service_company = request.GET.get("service_company")

    if service_company:
        claims = claims.filter(
            service_company_id = service_company
        )

    sort = request.GET.get("sort", "failure_date")

    allowed_sort_fields = {
        "failure_date",
        "-failure_date",
    }

    if sort not in allowed_sort_fields:
        sort = "failure_date"

    claims = claims.order_by(sort)

    failure_nodes = Directory.objects.filter(
        entity = Directory.Entity.FAILURE_NODE
    )

    recovery_methods = Directory.objects.filter(
        entity = Directory.Entity.RECOVERY_METHOD
    )

    service_companies =User.objects.filter(
        role = User.Role.SERVICE,
        is_active = True,
    )

    context = {
        "claims": claims,
        "failure_nodes": failure_nodes,
        "recovery_methods": recovery_methods,
        "service_companies": service_companies,
    }

    return render (
        request,
        "core/claim_list.html",
        context
    )

