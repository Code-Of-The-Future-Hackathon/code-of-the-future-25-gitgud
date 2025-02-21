from django.db import models


class Pet(models.Model):
    PET_TYPE = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('parrot', 'Parrot'),
        ('hamster', 'Hamster'),
        ('fish', 'Fish'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField()
    type = models.CharField(max_length=50, choices=PET_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
