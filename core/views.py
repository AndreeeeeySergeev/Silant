from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView

from .forms import MachineForm, MaintenanceForm, ClaimForm
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

    machine_serial_number = request.GET.get("machine")

    if machine_serial_number:
        maintenances = maintenances.filter(
            machine__serial_number = machine_serial_number
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
        "machine__serial_number",
        "-machine__serial_number",
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
        "current_sort": sort,
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

    service_companies = User.objects.filter(
        role = User.Role.SERVICE,
        is_active = True,
    )

    context = {
        "claims": claims,
        "failure_nodes": failure_nodes,
        "recovery_methods": recovery_methods,
        "service_companies": service_companies,
        "current_sort": sort,
    }

    return render (
        request,
        "core/claim_list.html",
        context
    )

@login_required
def machine_detail(request, pk):
    user = request.user

    if user.role == User.Role.MANAGER:
        machine = get_object_or_404(Machine, pk=pk)

    elif user.role == User.Role.CLIENT:
        machine = get_object_or_404(Machine, pk = pk, client = user)

    elif user.role == User.Role.SERVICE:
        machine = get_object_or_404(Machine, pk = pk, service_company = user)

    else:
        raise Http404

    context = {
        "machine": machine
    }

    return render(
        request,
        "core/machine_detail.html",
        context,
    )

@login_required
def maintenance_detail(request, pk):
    user = request.user

    if user.role == User.Role.MANAGER:
        maintenance = get_object_or_404(Maintenance, pk = pk)

    elif user.role == User.Role.CLIENT:
        maintenance = get_object_or_404(Maintenance, pk = pk, machine__client = user)

    elif user.role ==User.Role.SERVICE:
        maintenance = get_object_or_404(Maintenance, pk = pk, service_company = user)

    else:
        raise Http404

    context = {
        "maintenance": maintenance,
    }

    return render (
        request,
        "core/maintenance_detail.html",
        context,
    )

@login_required
def claim_detail(request, pk):
    user = request.user

    if user.role == User.Role.MANAGER:
        claim = get_object_or_404(Claim, pk = pk)

    elif user.role == User.Role.CLIENT:
        claim = get_object_or_404(Claim, pk = pk, machine__client = user)

    elif user.role == User.Role.SERVICE:
        claim = get_object_or_404(Claim, pk = pk, service_company = user)

    else:
        raise Http404

    context = {
        "claim": claim,
    }

    return render(
        request,
        "core/claim_detail.html",
        context
    )

@login_required
def machine_create(request):
    if request.user.role != User.Role.MANAGER:
        raise PermissionDenied

    if request.method == "POST":
        form = MachineForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("core:machine_list")

    else:
        form = MachineForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/machine_form.html",
        context
    )

@login_required
def maintenance_create(request):
    if request.user.role not in [
        User.Role.MANAGER,
        User.Role.CLIENT,
        User.Role.SERVICE,
    ]:
        raise PermissionDenied

    if request.method == "POST":
        form = MaintenanceForm(
            request.POST,
            user = request.user,
        )
        if form.is_valid():
            form.save()
            return redirect("core:maintenance_list")

    else:
        form = MaintenanceForm(user = request.user)

    context = {
        "form": form,
    }

    return render(
        request,
        "core/maintenance_form.html",
        context
    )

@login_required
def claim_create(request):
    if request.user.role not in [
        User.Role.SERVICE,
        User.Role.MANAGER
    ]:
        raise PermissionDenied

    if request.method == "POST":
        form = ClaimForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("core:claim_list")

    else:
        form = ClaimForm(
            user = request.user,
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "core/claim_form.html",
        context,
    )

def guest_machine_search(request):
    serial_number = request.GET.get("serial_number")

    machine = None
    message = None

    if serial_number:
        machine = Machine.objects.filter(
            serial_number = serial_number
        ).values(
            "serial_number",
            "machine_model__name",
            "engine_model__name",
            "engine_serial_number",
            "transmission_model__name",
            "transmission_serial_number",
            "drive_axle_model__name",
            "drive_axle_serial_number",
            "steering_axle_model__name",
            "steering_axle_serial_number",
        ).first()

        if not machine:
            message = (
                "Данных о машине с таким заводским номером нет в системе"
            )

    context = {
        "machine": machine,
        "serial_number": serial_number,
        "message": message,
    }

    return render(
        request,
        "core/home.html",
        context,
    )

class UserLoginView(LoginView):
    template_name = "core/login.html"
    next_page = "core:machine_list"

class UserLogoutView(LogoutView):
    next_page = "core:login"

def home(request):
    return render(
        request,
        "core/home.html"
    )