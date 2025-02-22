from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, FoodLog, WaterLog, DoorLog


@login_required
def dashboard(request):
    owner_pets = Pet.objects.filter(owner=request.user)

    # if current time is between Pet.door_open_time and Pet.door_close_time, including, then the door is open
    for pet in owner_pets:
        if pet.door_open_time and pet.door_close_time and pet.door_mode == 'automatic':
            current_time = datetime.now().time()
            print(current_time, pet.door_open_time, pet.door_close_time)
            print(pet.door_open_time <= current_time <= pet.door_close_time)
            if pet.door_open_time <= current_time <= pet.door_close_time:
                doorlog = DoorLog(pet=pet, direction='in', status='open', mode='automatic')
                doorlog.save()
            else:
                doorlog = DoorLog(pet=pet, direction='out', status='close', mode='automatic')
                doorlog.save()

    context = {
        'owner_pets': owner_pets,
    }

    return render(request, 'dashboard/dashboard.html', context)


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import datetime, time
from .models import Pet

def manage_food_water(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        # Get string values (fallback to current pet values if not provided)
        food_mode = request.POST.get('food_mode', pet.food_mode)
        automatic_food_mode = request.POST.get('automatic_food_mode', pet.automatic_food_mode)
        automatic_food_time = request.POST.get('automatic_food_time', '')
        automatic_food_interval = request.POST.get('automatic_food_interval', '')
        automatic_food_quantity = request.POST.get('automatic_food_quantity', '')

        water_mode = request.POST.get('water_mode', pet.water_mode)
        automatic_water_mode = request.POST.get('automatic_water_mode', pet.automatic_water_mode)
        automatic_water_time = request.POST.get('automatic_water_time', '')
        automatic_water_interval = request.POST.get('automatic_water_interval', '')
        automatic_water_quantity = request.POST.get('automatic_water_quantity', '')

        pet.food_mode = food_mode
        pet.water_mode = water_mode
        pet.automatic_food_mode = automatic_food_mode
        pet.automatic_water_mode = automatic_water_mode

        # Parse time fields for food
        try:
            if automatic_food_time:
                pet.automatic_food_time = datetime.strptime(automatic_food_time, "%H:%M").time()
            else:
                pet.automatic_food_time = time(12, 0)
        except (ValueError, TypeError):
            pet.automatic_food_time = time(12, 0)

        # Parse time fields for water
        try:
            if automatic_water_time:
                pet.automatic_water_time = datetime.strptime(automatic_water_time, "%H:%M").time()
            else:
                pet.automatic_water_time = time(12, 0)
        except (ValueError, TypeError):
            pet.automatic_water_time = time(12, 0)

        # Parse numeric fields for food interval
        try:
            pet.automatic_food_interval = int(automatic_food_interval)
        except (ValueError, TypeError):
            pet.automatic_food_interval = 0

        # Parse numeric fields for food quantity
        try:
            pet.automatic_food_quantity = int(automatic_food_quantity)
        except (ValueError, TypeError):
            pet.automatic_food_quantity = 0

        # Parse numeric fields for water interval
        try:
            pet.automatic_water_interval = int(automatic_water_interval)
        except (ValueError, TypeError):
            pet.automatic_water_interval = 0

        # Parse numeric fields for water quantity
        try:
            pet.automatic_water_quantity = int(automatic_water_quantity)
        except (ValueError, TypeError):
            pet.automatic_water_quantity = 0

        pet.save()
        messages.success(request, 'Food and water settings updated')
        return redirect("manage_food_water", id=id)

    context = {
        'pet': pet,
    }
    return render(request, 'dashboard/manage_food_water.html', context)


def manage_door(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        door_mode = request.POST.get('door_mode', pet.door_mode)
        always_open = request.POST.get('always_open')
        door_open_time = request.POST.get('door_open_time')
        door_close_time = request.POST.get('door_close_time')
        in_house = request.POST.get('in_house')
        allow_in_after_closing = request.POST.get('allow_in_after_closing')

        # Update door_mode (ensure it's one of the expected values)
        if door_mode in ['manual', 'automatic']:
            pet.door_mode = door_mode
        else:
            pet.door_mode = pet.door_mode

        # For checkboxes, typical values are "on" if checked.
        pet.always_open = True if always_open in ['on', 'true', '1'] else False

        # Parse door_open_time; default to 08:00 if missing/invalid.
        try:
            if door_open_time:
                pet.door_open_time = datetime.strptime(door_open_time, "%H:%M").time()
            else:
                pet.door_open_time = time(8, 0)
        except (ValueError, TypeError):
            pet.door_open_time = time(8, 0)

        # Parse door_close_time; default to 20:00 if missing/invalid.
        try:
            if door_close_time:
                pet.door_close_time = datetime.strptime(door_close_time, "%H:%M").time()
            else:
                pet.door_close_time = time(20, 0)
        except (ValueError, TypeError):
            pet.door_close_time = time(20, 0)

        pet.allow_in_after_closing = True if allow_in_after_closing in ['on', 'true', '1'] else False

        pet.save()

        # create log from current data
        doorlog = DoorLog(pet=pet, direction='in', status='open', mode=door_mode)
        doorlog.save()

        messages.success(request, 'Door settings updated')
        return redirect("manage_door", id=id)

    context = {'pet': pet}
    return render(request, 'dashboard/manage_door.html', context)


def manual_door(request, id):
    pet = get_object_or_404(Pet, id=id)
    latestdoorlog = pet.door_logs.last()
    if request.method == "POST":
        status = request.POST.get('status')
        print(status)
        if status == 'open':
            doorlog = DoorLog(pet=pet, direction='in', status='open', mode='manual')
            doorlog.save()
            return HttpResponse("success")
        else:
            doorlog = DoorLog(pet=pet, direction='out', status='close', mode='manual')
            doorlog.save()
            return HttpResponse("success")

    return HttpResponse("Invalid request")


def manage_location(request, id):

    pet = get_object_or_404(Pet, id=id)

    context = {
        'pet': pet,
    }

    return render(request, 'dashboard/manage_location.html', context)