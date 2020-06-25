# Links to files:
#
# * [[admin.py]]
# * [[apps.py]]
# * [[forms.py]]
# * [[models.py]]
# * [[tests.py]]
# * [[urls.py]]
# * [[views.py]]
# * [[app.js]]
# * [[constants.py]]

from django.db import models


class Standard(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=30)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    t_min = models.FloatField()
    t_max = models.FloatField()

    def __str__(self):
        return self.name


class PressureClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# TODO add pressures for all temperatures
class Pressure(models.Model):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    pressure_class = models.ForeignKey(PressureClass, on_delete=models.CASCADE)
    pressure_m29 = models.FloatField()
    pressure_38 = models.FloatField()
    pressure_50 = models.FloatField()
    pressure_100 = models.FloatField()
    pressure_150 = models.FloatField()
    pressure_200 = models.FloatField()
    pressure_250 = models.FloatField()
    pressure_300 = models.FloatField()
    pressure_325 = models.FloatField()
    pressure_350 = models.FloatField()
    pressure_375 = models.FloatField()
    pressure_400 = models.FloatField()
    pressure_425 = models.FloatField()

    def __str__(self):
        return str(self.name)


class Results(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    pressure_class = models.ForeignKey(PressureClass, on_delete=models.CASCADE)
