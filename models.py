from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return self.name