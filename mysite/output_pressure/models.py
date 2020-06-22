from django.db import models


# Create your models here.

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
    material_class = models.ForeignKey(PressureClass, on_delete=models.CASCADE)
    pressure_m29 = models.FloatField()
    pressure_38 = models.FloatField()
    pressure_50 = models.FloatField()
    pressure_100 = models.FloatField()
    pressure_150 = models.FloatField()

    def __str__(self):
        return str(self.name)


class Results(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    pressure_class = models.ForeignKey(PressureClass, on_delete=models.CASCADE)
