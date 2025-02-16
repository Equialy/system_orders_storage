# Generated by Django 4.2 on 2025-02-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_dish_remove_orders_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dish',
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('В ожидании', 'В ожидании'), ('Готово', 'Готово'), ('Оплачено', 'Оплачено')], default='В ожидании', max_length=10),
        ),
    ]
