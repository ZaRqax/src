# Generated by Django 4.1.7 on 2023-03-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0003_attributevalue'),
        ('entities', '0003_entity'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='attributes',
            field=models.ManyToManyField(related_name='entities', through='attributes.AttributeValue', to='attributes.attribute', verbose_name='Атрибуты'),
        ),
    ]
