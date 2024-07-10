from django.db import models

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    class_rooms = models.ManyToManyField('ClassRoom')
    deleted = models.BooleanField(default=False)

class ClassRoom(models.Model):
    benches = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()

class Student(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    division = models.CharField(max_length=10)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.DO_NOTHING, null=True)