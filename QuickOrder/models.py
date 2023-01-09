from django.db import models

class PeopleGroupType(models.Model): 
    name = models.TextField()
    status = models.BooleanField(default=True)
    numberOfPeople = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class Diet(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class FoodType(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name