# Generated by Django 3.0.7 on 2020-06-18 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('output_pressure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='standard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='output_pressure.Standard'),
        ),
    ]
