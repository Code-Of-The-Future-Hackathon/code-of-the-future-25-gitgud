from django.contrib import admin
from .models import Pet, DoorLog, FoodLog, WaterLog, LocationLog

admin.site.register(Pet)
admin.site.register(DoorLog)
admin.site.register(FoodLog)
admin.site.register(WaterLog)
admin.site.register(LocationLog)
