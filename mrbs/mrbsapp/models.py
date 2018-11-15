from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class Usr(AbstractUser):
    tel = models.CharField(max_length=32)

class Room(models.Model):
    caption = models.CharField(max_length=32)
    num = models.IntegerField()

    def __str__(self):
        return self.caption


class Book(models.Model):
    user = models.ForeignKey(to="Usr",on_delete=models.CASCADE)
    room = models.ForeignKey(to="Room", on_delete=models.CASCADE)
    date = models.DateField()
    choices = (
        (1,'8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    time_id = models.IntegerField(choices=choices)

    class Meta:
        unique_together = (("room","date","time_id"),)

    def __str__(self):
        return str(self.user)+" book " + str(self.room)
