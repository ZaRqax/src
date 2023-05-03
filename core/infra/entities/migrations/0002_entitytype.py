# Generated by Django 4.1.7 on 2023-03-13 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attributes', '0002_attribute'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Поле будет изменено при обновлении любого из полей модели.', null=True, verbose_name='Дата последнего обновления')),
                ('title', models.CharField(max_length=1024, verbose_name='Название типа объекта')),
                ('attributes', models.ManyToManyField(related_name='entity_types', to='attributes.attribute', verbose_name='Атрибуты')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entity_types', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entities.typegrade', verbose_name='Грейд типа объекта')),
            ],
            options={
                'verbose_name': 'Тип объекта',
                'verbose_name_plural': 'Типы объектов',
            },
        ),
    ]