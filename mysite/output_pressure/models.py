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
    standard = models.ForeignKey(Standard, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class MaterialClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Pressure(models.Model):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    material_class = models.ForeignKey(MaterialClass, on_delete=models.CASCADE)
    temperature_50 = models.FloatField()
    temperature_100 = models.FloatField()
    temperature_150 = models.FloatField()

    def __str__(self):
        return str(self.name)


class OutputPressure(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    material_class = models.ForeignKey(MaterialClass, on_delete=models.SET_NULL, null=True)
