from django.db import models

class City(models.Model):
    city_name = models.CharField(max_length=200)

    def __str__(self):
        return self.city_name
