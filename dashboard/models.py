import uuid

from django.db import models


class Pet(models.Model):
    PET_TYPE = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('parrot', 'Parrot'),
        ('hamster', 'Hamster'),
        ('fish', 'Fish'),
        ('dragon', 'Dragon'),
        ('other', 'Other'),
    )

    MODES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    )

    AUTO_MODES = (
        ("timed", "Timed"),
        ("interval", "Interval"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    dob = models.DateField(default=None, null=True)
    exact_birthday = models.BooleanField(default=False)
    age = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=PET_TYPE)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    food_mode = models.CharField(max_length=50, choices=MODES, default='automatic')
    water_mode = models.CharField(max_length=50, choices=MODES, default='automatic')

    automatic_food_mode = models.CharField(max_length=50, choices=AUTO_MODES, default='timed')
    automatic_food_interval = models.IntegerField(default=0)
    automatic_food_time = models.TimeField(null=True, blank=True)
    automatic_food_quantity = models.IntegerField(default=0)

    automatic_water_mode = models.CharField(max_length=50, choices=AUTO_MODES, default='timed')
    automatic_water_interval = models.IntegerField(default=0)
    automatic_water_time = models.TimeField(null=True, blank=True)
    automatic_water_quantity = models.IntegerField(default=0)

    door_mode = models.CharField(max_length=50, choices=MODES, default='automatic')
    always_open = models.BooleanField(default=False)
    door_open_time = models.TimeField(null=True, blank=True)
    door_close_time = models.TimeField(null=True, blank=True)
    in_house = models.BooleanField(default=True)
    allow_in_after_closing = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class DoorLog(models.Model):
    DIRECTION = (
        ('in', 'In'),
        ('out', 'Out'),
    )

    STATUS = (
        ('open', 'Open'),
        ('close', 'Close'),
    )

    MODE = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='door_logs')

    direction = models.CharField(max_length=50, choices=DIRECTION, default='in')
    status = models.CharField(max_length=50, choices=STATUS, default='close')

    mode = models.CharField(max_length=50, choices=MODE, default='automatic')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.created_at}"


class FoodLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='food_logs')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return f"{self.pet.name} - {self.created_at}"


class WaterLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='water_logs')
    quantity = models.IntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.pet.name} - {self.created_at}"


class LocationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='location_logs')
    text = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.created_at}"
