from django.db import models

# Create your models here.


class Booking(models.Model):
    name = models.CharField(max_length=255, null=True)
    guest_number = models.SmallIntegerField(default=1)
    date = models.DateField(null=True)
    comment = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.name} : {str(self.date)}'


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} : {str(self.price)}'


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    menu_item_description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name
