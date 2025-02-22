import random
import uuid
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Pet, FoodLog, WaterLog, DoorLog, LocationLog


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
from datetime import datetime, time, timedelta
from .models import Pet


def manage_food_water(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        # --- UPDATE PET SETTINGS (unchanged logic) ---
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

        # Parse numeric fields for intervals and quantities
        try:
            pet.automatic_food_interval = int(automatic_food_interval)
        except (ValueError, TypeError):
            pet.automatic_food_interval = 0

        # Convert percentage to grams if between 0 and 100
        try:
            qty = int(automatic_food_quantity)
        except (ValueError, TypeError):
            pet.automatic_food_quantity = 0

        try:
            pet.automatic_water_interval = int(automatic_water_interval)
        except (ValueError, TypeError):
            pet.automatic_water_interval = 0

        try:
            pet.automatic_water_quantity = int(automatic_water_quantity)
        except (ValueError, TypeError):
            pet.automatic_water_quantity = 0

        pet.save()
        messages.success(request, 'Food and water settings updated')
        return redirect("manage_food_water", id=id)

    # -------------------------------------------------------
    #                 IMPROVED CONSUMPTION LOGIC
    # -------------------------------------------------------
    one_week_ago = timezone.now() - timedelta(days=7)

    #
    # 1) FOOD CONSUMPTION
    #
    food_logs = (
        pet.food_logs
        .filter(created_at__gte=one_week_ago)
        .order_by('created_at')
    )

    # We'll accumulate consumption by (date -> total_consumed).
    # For daily grouping, we can map each date to the total consumption.
    # E.g., { '2025-02-15': 150g, '2025-02-16': 80g, ... }
    food_consumption_by_day = defaultdict(float)
    previous_log = None

    for log in food_logs:
        if previous_log is not None:
            # If quantity has decreased, that difference is consumed
            if previous_log.quantity > log.quantity:
                consumption = previous_log.quantity - log.quantity
                # Group by the *day* of the previous_log or the current log?
                # Typically we group by the day we noticed the consumption,
                # so let's use log.created_at.date().
                day_str = log.created_at.date().isoformat()
                food_consumption_by_day[day_str] += consumption
        previous_log = log

    # Total consumption over last 7 days:
    total_consumption_7d = sum(food_consumption_by_day.values())

    # Average daily consumption:
    # Count how many days we actually have data for, to avoid dividing by 7
    # if logs exist for fewer days.
    days_of_logs = len(food_consumption_by_day)
    if days_of_logs == 0:
        average_daily_food = 0
    else:
        average_daily_food = total_consumption_7d / days_of_logs

    # Now predict usage:
    # Next 7 days
    predicted_food_week = average_daily_food * 7
    # Next 30 days
    predicted_food_month = average_daily_food * 30
    # Next 90 days
    predicted_food_quarter = average_daily_food * 90

    #
    # 2) WATER CONSUMPTION
    #
    water_logs = (
        pet.water_logs
        .filter(created_at__gte=one_week_ago)
        .order_by('created_at')
    )

    water_consumption_by_day = defaultdict(float)
    previous_log = None

    for log in water_logs:
        if previous_log is not None:
            if previous_log.quantity > log.quantity:
                consumption = previous_log.quantity - log.quantity
                day_str = log.created_at.date().isoformat()
                water_consumption_by_day[day_str] += consumption
        previous_log = log

    total_water_7d = sum(water_consumption_by_day.values())
    days_of_water_logs = len(water_consumption_by_day)
    if days_of_water_logs == 0:
        average_daily_water = 0
    else:
        average_daily_water = total_water_7d / days_of_water_logs

    predicted_water_week = average_daily_water * 7
    predicted_water_month = average_daily_water * 30
    predicted_water_quarter = average_daily_water * 90

    #
    # Debug prints or logs
    #
    print("FOOD -> 7d:", total_consumption_7d,
          "daily avg:", average_daily_food,
          "predictions:", predicted_food_week,
          predicted_food_month,
          predicted_food_quarter)

    print("WATER -> 7d:", total_water_7d,
          "daily avg:", average_daily_water,
          "predictions:", predicted_water_week,
          predicted_water_month,
          predicted_water_quarter)

    #
    # 3) Render context
    #
    context = {
        'pet': pet,
        'last_week_food': total_consumption_7d,
        'last_week_water': total_water_7d,
        'predicted_food_week': predicted_food_week,
        'predicted_food_month': predicted_food_month,
        'predicted_food_quarter': predicted_food_quarter,
        'predicted_water_week': predicted_water_week,
        'predicted_water_month': predicted_water_month,
        'predicted_water_quarter': predicted_water_quarter,
    }
    return render(request, 'dashboard/manage_food_water.html', context)


def temp_generate_food_log(request, id):
    """Generate 2 weeks of hourly water logs, ~750 ml/day via ~2 daily refills."""
    pet = get_object_or_404(Pet, id=id)

    # We'll log from 14 days ago up to 'now'
    end_date = timezone.now()
    start_date = end_date - timedelta(days=14)

    # We track the current hour in this loop
    current_time = start_date
    # Start the bowl at 100% (which is 400 ml full)
    current_quantity = 100

    # We'll store new WaterLog objects in memory first, then bulk-create them
    logs_to_create = []

    while current_time <= end_date:
        hour = current_time.hour

        # Refill at 07:00 and 19:00
        if hour == 7 or hour == 19:
            current_quantity = 100
        else:
            # Random usage between 5–11% each hour
            usage_percent = random.randint(5, 11)
            current_quantity -= usage_percent
            if current_quantity < 0:
                current_quantity = 0

        # Build WaterLog object (don't save individually)
        water_log = WaterLog(
            id=uuid.uuid4(),
            pet=pet,
            quantity=current_quantity,  # 0–100
            created_at=current_time  # works only if not auto_now_add
        )
        logs_to_create.append(water_log)

        # Increment by one hour
        current_time += timedelta(hours=1)

    # Bulk-insert all logs
    WaterLog.objects.bulk_create(logs_to_create)

    return HttpResponse("Water logs (~750 ml/day) generated successfully!")


def manage_door(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == 'POST':
        door_mode = request.POST.get('door_mode', pet.door_mode)
        always_open = request.POST.get('always_open')
        door_open_time = request.POST.get('door_open_time')
        door_close_time = request.POST.get('door_close_time')
        in_house = request.POST.get('in_house')
        allow_in_after_closing = request.POST.get('allow_in_after_closing')

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


def location_history(request, id):
    # Example: last 7 days, then get the most recent 10 from those
    one_week_ago = timezone.now() - timedelta(days=7)

    locationlogs = (
        LocationLog.objects.filter(created_at__gte=one_week_ago, pet__id=id)
        .order_by('-created_at')[:10]
    )
    # If you need them in chronological order for correct path visualization:
    locationlogs = sorted(locationlogs, key=lambda x: x.created_at)

    context = {
        'locationlogs': locationlogs
    }
    return render(request, 'dashboard/location_history.html', context)


def map_test(request):
    return render(request, 'dashboard/map_test.html')


def add_pet(request):
    if request.method == "POST":
        name = request.POST.get('name')
        typeD = request.POST.get('type')
        exact_birthday = request.POST.get('exact_birthday')
        age = request.POST.get('age')
        birthday = request.POST.get('birthday')

        if exact_birthday:
            pet = Pet(name=name, type=typeD, dob=birthday, owner=request.user)
        else:
            pet = Pet(name=name, type=typeD, age=age, owner=request.user)

        messages.success(request, 'Pet added successfully')
        pet.save()

    return render(request, 'dashboard/add_pet.html')
